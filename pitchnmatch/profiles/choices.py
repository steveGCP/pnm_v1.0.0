from django.db import models

class Role(models.TextChoices):
    FOUNDER = 'founder', 'Fondateur'
    INVESTOR = 'investor', 'Investisseur'
    MENTOR = 'mentor', 'Mentor'
    TALENT = 'talent', 'Talent'
    PARTNER = 'partner', 'Partenaire'

class Stage(models.TextChoices):
    IDEA = 'idea', 'Idée'
    PROTOTYPE = 'prototype', 'Prototype / MVP'
    CUSTOMERS = 'customers', 'Premiers clients'
    REVENUE = 'revenue', 'Revenus'
    GROWTH = 'growth', 'Croissance'

class Availability(models.TextChoices):
    FULL_TIME = 'full_time', 'Temps plein'
    PART_TIME = 'part_time', 'Temps partiel'
    PUNCTUAL = 'punctual', 'Ponctuel'

class BusinessModel(models.TextChoices):
    B2B = 'b2b', 'B2B (Business to Business)'
    B2C = 'b2c', 'B2C (Business to Consumer)'
    B2G = 'b2g', 'B2G (Business to Government)'
    B2B2C = 'b2b2c', 'B2B2C'
