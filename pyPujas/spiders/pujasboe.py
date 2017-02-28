# -*- coding: utf-8 -*-
import scrapy
from pyPujas.items import PypujasItem
import urllib.parse


row_ids_dict = {
    'Identificador': 'id_puja',
    'Tipo de subasta': 'type_puja',
    'Fecha de inicio': 'start_date',
    'Fecha de conclusión': 'end_date',
    'Cantidad reclamada': 'debt',
    'Lotes': 'lots',
    'Valor subasta': 'value',
    'Puja mínima': 'min_puja',
    'Descripción': 'property_description',
    'Referencia catastral': 'property_registry',
    'Dirección': 'property_address',
    'Código Postal': 'property_zipcode',
    'Localidad': 'property_town',
    'Provincia': 'property_province',
    'Vivienda habitual': 'is_habitual_residence',
    'Inscripción registral': 'property_registration'
}


class PujasboeSpider(scrapy.Spider):
    name = 'pujasboe'
    allowed_domains = ['subastas.boe.es']
    start_urls = [
        'https://subastas.boe.es/reg/subastas_ava.php?campo%5B0%5D=SUBASTA.ORIGEN&dato%5B0%5D=&campo%5B1%5D=SUBASTA.ESTADO&dato%5B1%5D=&campo%5B2%5D=BIEN.TIPO&dato%5B2%5D=I&campo%5B4%5D=BIEN.DIRECCION&dato%5B4%5D=&campo%5B5%5D=BIEN.CODPOSTAL&dato%5B5%5D=&campo%5B6%5D=BIEN.LOCALIDAD&dato%5B6%5D=&campo%5B7%5D=BIEN.COD_PROVINCIA&dato%5B7%5D=33&campo%5B8%5D=SUBASTA.POSTURA_MINIMA_MINIMA_LOTES&dato%5B8%5D=&campo%5B9%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_1&dato%5B9%5D=&campo%5B10%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_2&dato%5B10%5D=&campo%5B11%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_3&dato%5B11%5D=&campo%5B12%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_4&dato%5B12%5D=&campo%5B13%5D=SUBASTA.NUM_CUENTA_EXPEDIENTE_5&dato%5B13%5D=&campo%5B14%5D=SUBASTA.ID_SUBASTA_BUSCAR&dato%5B14%5D=&campo%5B15%5D=SUBASTA.FECHA_FIN_YMD&dato%5B15%5D%5B0%5D=&dato%5B15%5D%5B1%5D=&campo%5B16%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&page_hits=40&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar',
    ]
   
    def parse(self, response):
        # Get iterable URL of current search results
        url = response.xpath('//ul[@class="navlist"]/li/a[@class="current"]/@href').extract()[0]
        # Detect position of first '-' char in URL
        pos = url.index('-')
        # Remove that data from URL
        url = url[:pos] + '-{}-{}'
        
        # Get the number of search results
        results_text = response.xpath('//div[@class="paginar"]/ul/li/text()').extract()[0]
        n_results = int(results_text.split()[-1])
        results_per_page = 40
        start_result = 0
        
        # Start visiting each page of 40 results and parsing its contents
        while start_result < n_results:
            next_url = urllib.parse.urljoin('https://' + self.allowed_domains[0], url.format(start_result, results_per_page))
            start_result += results_per_page
            yield scrapy.Request(next_url, self.parse_results)
        
    def parse_results(self, response):
        items = []
        # Get the link for each puja, and use parse_puja as a callback for those requests
        links_pujas = response.xpath('//div[@class="enlacesMas"]/a[@class="resultado-busqueda-link-defecto"]/@href').extract()
        for url in links_pujas:
            item = PypujasItem()
            full_url = urllib.parse.urljoin('https://' + self.allowed_domains[0], url)
            request = scrapy.Request(url=full_url, callback=self.parse_table_puja, meta={'item': item})
            request.meta['item'] = item
            yield request
            
            # There is additional data in other tabs, where URL just changes in parameter "&ver=x&"
            additional_url = full_url.replace('&ver=1&', '&ver=3&')
            request = scrapy.Request(url=additional_url, callback=self.parse_table_puja, meta={'item': item})
            request.meta['item'] = item
            yield request
            
            additional_url = full_url.replace('&ver=1&', '&ver=6&')
            request = scrapy.Request(url=additional_url, callback=self.parse_amounts_puja, meta={'item': item})
            yield request
            
    def parse_table_puja(self, response):
        item = response.meta['item']
        table_rows = response.xpath('//table[@class="datosSubastas"]/tr')

        for row in table_rows:
            try:
                row_id = row.xpath('th/text()').extract()[0]
                row_value = row.xpath('td/strong/text()|td/text()').extract()[0].strip().rstrip()
                if not row_value:
                    print('coco-1')
                    row_value = row.xpath('td/strong/text()').extract()[0].strip().rstrip()
                if not row_value:
                    print('coco-2')
                    row_value = row.xpath('td/a/@href').extract()[0]
                    
                print('ROW: ', row_id, row_value)
                
                if row_id in row_ids_dict.keys():
                    item[row_ids_dict[row_id]] = row_value
            except Exception as err:
                print('ERROR: ' + str(err))
        
        return item

    def parse_amounts_puja(self, response):
        item = response.meta['item']
        highest_bid = response.xpath('//div[@class="bloqueSubasta"]/h3[*="Puja más alta en esta subasta"]/following::p/span[@class="destacaNegrita"]/text()').extract()[0]
        item['highest_bid'] = 0 if(highest_bid == 'Subasta sin pujas') else highest_bid
        return item