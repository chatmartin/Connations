
class Country:
    name:str
    flag_color:list
    star:bool
    coat_of_arms:bool
    borders:list
    official_lang:list
    island:bool
    landlocked:bool
    equator:bool
    gdp:bool
    pop:bool
    cup_host:bool
    olympic_host:bool
    european_union:bool
    ussr:bool
    commonwealth:bool
    brics:bool
    monarchy:bool
    mult_timezones:bool
    cap_pop:bool
    maj_relig:str
    left_side:bool
    region:str

    def __init__(self,name,flag_color,star,coat_of_arms,borders,official_lang,island,landlocked,equator,gdp,pop,cup_host,olympic_host,european_union,ussr,commonwealth,brics,monarchy,mult_timezones,cap_pop,maj_relig,left_side,region):
        self.name = name
        self.flag_color=flag_color
        self.star=star
        self.coat_of_arms=coat_of_arms
        self.borders=borders
        self.official_lang=official_lang
        self.island=island
        self.landlocked=landlocked
        self.equator=equator
        self.gdp=gdp
        self.pop=pop
        self.cup_host=cup_host
        self.olympic_host=olympic_host
        self.european_union = european_union
        self.ussr = ussr
        self.commonwealth = commonwealth
        self.brics = brics
        self.monarchy = monarchy
        self.mult_timezones = mult_timezones
        self.cap_pop = cap_pop
        self.maj_relig = maj_relig
        self.left_side = left_side
        self.region = region

    def get_name(self):
        return self.name

    def get_flag_color(self):
        return self.flag_color

    def get_star(self):
        return self.star

    def get_coat_of_arms(self):
        return self.coat_of_arms

    def get_brics(self):
        return self.brics

    def get_borders(self):
        return self.borders

    def get_region(self):
        return self.region

    def ge_tofficial_lang(self):
        return self.official_lang

    def get_island(self):
        return self.island

    def get_landlocked(self):
        return self.landlocked

    def get_equator(self):
        return self.equator

    def get_gdp(self):
        return self.gdp

    def get_pop(self):
        return self.pop

    def get_cup_host(self):
        return self.cup_host

    def get_olympic_host(self):
        return self.olympic_host

    def get_european_union(self):
        return self.european_union

    def get_ussr(self):
        return self.ussr

    def get_commonwealth(self):
        return self.commonwealth

    def get_monarchy(self):
        return self.monarchy

    def get_mult_timezones(self):
        return self.mult_timezones

    def get_cap_pop(self):
        return self.cap_pop

    def get_maj_relig(self):
        return self.maj_relig

    def get_left_side(self):
        return self.left_side



