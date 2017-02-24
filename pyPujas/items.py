# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class PypujasItem(scrapy.Item):
    id_puja = scrapy.Field()                    # Identificador
    link = scrapy.Field()                       # URL de la puja
    type_puja = scrapy.Field()                  # Tipo de subasta
    start_date = scrapy.Field()                 # Fecha de inicio
    end_date = scrapy.Field()                   # Fecha de conclusion
    debt = scrapy.Field()                       # Cantidad reclamada
    lots = scrapy.Field()                       # Lotes
    value = scrapy.Field()                      # Valor subasta
    min_puja = scrapy.Field()                   # Puja minima
    creditor = scrapy.Field()                   # Nombre del acreedor
    property_type = scrapy.Field()              # Tipo de propiedad
    property_registry = scrapy.Field()          # Referencia catastral
    property_address = scrapy.Field()           # Direccion
    property_description = scrapy.Field()       # Descripcion
    property_town = scrapy.Field()              # Localidad
    property_zipcode = scrapy.Field()           # Codigo Postal
    property_province = scrapy.Field()          # Provincia
    property_registration = scrapy.Field()      # Inscripcion registral
    is_habitual_residence = scrapy.Field()      # Vivienda habitual
    max_puja = scrapy.Field()                   # Maxima puja hasta el momento
    status = scrapy.Field()                     # Estado de la puja: abierta, futura, cerrada...
