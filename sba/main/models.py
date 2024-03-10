from django.contrib.auth.models import AbstractUser
from django.db import models

# Ceci est un modèle utilisateur personnalisé qui hérite actuellement de AbstractUser.
# Il est prêt à être étendu avec des champs et méthodes supplémentaires si besoin.(comme birth_date ici)
# Si aucun champ supplémentaire n'est requis au-delà du modèle par défaut de Django,
# cette classe peut rester vide et AbstractUser sera utilisé comme tel. 
class User(AbstractUser):
    birth_date = models.DateField(auto_now=False, null=True)
    

#stocker les informations de l'api en bdd
class PredApi(models.Model):

    NEW_EXIST_CHOICES = (
        (1, 'Existing business'),
        (2, 'New business'),
    )
    URBANRURAL_CHOICES = (
        (1, 'Urban'),
        (2, 'Rural'),
        (0, 'Undefined'),
    )
    REVLINECR_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    LOWDOC_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    STATE_CHOICES = (
    ('IN', 'Indiana'), ('CT', 'Connecticut'), ('NJ', 'New Jersey'), ('FL', 'Florida'), 
    ('NC', 'North Carolina'), ('IL', 'Illinois'), ('OK', 'Oklahoma'), ('AR', 'Arkansas'), 
    ('MN', 'Minnesota'), ('CA', 'California'), ('SC', 'South Carolina'), ('TX', 'Texas'), 
    ('LA', 'Louisiana'), ('IA', 'Iowa'), ('OH', 'Ohio'), ('TN', 'Tennessee'), ('MS', 'Mississippi'), 
    ('MD', 'Maryland'), ('VA', 'Virginia'), ('MA', 'Massachusetts'), ('PA', 'Pennsylvania'), 
    ('OR', 'Oregon'), ('ME', 'Maine'), ('KS', 'Kansas'), ('MI', 'Michigan'), ('AK', 'Alaska'), 
    ('WA', 'Washington'), ('CO', 'Colorado'), ('WY', 'Wyoming'), ('UT', 'Utah'), ('WV', 'West Virginia'), 
    ('MO', 'Missouri'), ('AZ', 'Arizona'), ('ID', 'Idaho'), ('RI', 'Rhode Island'), ('NY', 'New York'), 
    ('NH', 'New Hampshire'), ('NM', 'New Mexico'), ('NV', 'Nevada'), ('ND', 'North Dakota'), 
    ('VT', 'Vermont'), ('WI', 'Wisconsin'), ('MT', 'Montana'), ('AL', 'Alabama'), ('GA', 'Georgia'), 
    ('KY', 'Kentucky'), ('NE', 'Nebraska'), ('SD', 'South Dakota'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), 
    ('HI', 'Hawaii'),
    )
    BANK_STATE_CHOICES = (
    ('OH', 'Ohio'), ('IN', 'Indiana'), ('DE', 'Delaware'), ('SD', 'South Dakota'), 
    ('AL', 'Alabama'), ('FL', 'Florida'), ('GA', 'Georgia'), ('OR', 'Oregon'), 
    ('MN', 'Minnesota'), ('NC', 'North Carolina'), ('MS', 'Mississippi'), 
    ('SC', 'South Carolina'), ('TX', 'Texas'), ('LA', 'Louisiana'), ('IA', 'Iowa'), 
    ('CA', 'California'), ('TN', 'Tennessee'), ('VA', 'Virginia'), ('MA', 'Massachusetts'), 
    ('RI', 'Rhode Island'), ('PA', 'Pennsylvania'), ('MO', 'Missouri'), ('WA', 'Washington'), 
    ('UT', 'Utah'), ('IL', 'Illinois'), ('WV', 'West Virginia'), ('KS', 'Kansas'), 
    ('WI', 'Wisconsin'), ('NJ', 'New Jersey'), ('NY', 'New York'), ('CT', 'Connecticut'), 
    ('MD', 'Maryland'), ('NH', 'New Hampshire'), ('ND', 'North Dakota'), ('MT', 'Mont')
    )

    State = models.CharField(max_length=2, choices=STATE_CHOICES)
    BankState = models.CharField(max_length=2, choices=BANK_STATE_CHOICES)
    RevLineCr = models.CharField(max_length=1,choices=REVLINECR_CHOICES)
    LowDoc = models.CharField(max_length=1,choices=LOWDOC_CHOICES)
    NewExist = models.IntegerField(choices=NEW_EXIST_CHOICES)
    UrbanRural = models.IntegerField(choices=URBANRURAL_CHOICES)
    FranchiseCode = models.IntegerField()
    FranchiseBinary = models.IntegerField(blank=True, null=True)
    Zip = models.IntegerField()
    Term = models.IntegerField()
    NoEmp = models.IntegerField()
    CreateJob = models.IntegerField()
    RetainedJob = models.IntegerField()
    GrAppv = models.FloatField()
    SBA_Appv = models.FloatField()
    #stocker la prédiction elle-même
    Prediction = models.IntegerField(null=True, blank=True)  #null et blank=True pour permettre de sauvegarder sans prédiction initialement
    NAICS = models.IntegerField()
    Industry = models.CharField(max_length=50, blank=True, null=True)  

    def save(self, *args, **kwargs):
        #defini franchiseBinary en fonction de franchiseCode
        if self.FranchiseCode == 0 or self.FranchiseCode == 1:
            self.FranchiseBinary = 0  # no franchise
        else:
            self.FranchiseBinary = 1  # franchise présente
        self.Industry = self.map_naics_to_industry()
        super().save(*args, **kwargs)

    def map_naics_to_industry(self):
        mapping = {
            11: 'Ag/For/Fish/Hunt',
            21: 'Min/Quar/Oil_Gas_ext',
            22: 'Utilities',
            23: 'Construction',
            31: 'Manufacturing',
            32: 'Manufacturing',
            33: 'Manufacturing',
            42: 'Wholesale_trade',
            44: 'Retail_trade',
            45: 'Retail_trade',
            48: 'Trans/Ware',
            49: 'Trans/Ware',
            51: 'Information',
            52: 'Finance/Insurance',
            53: 'RE/Rental/Lease',
            54: 'Prof/Science/Tech',
            55: 'Mgmt_comp',
            56: 'Admin_sup/Waste_Mgmt_Rem',
            61: 'Educational',
            62: 'Healthcare/Social_assist',
            71: 'Arts/Entertain/Rec',
            72: 'Accom/Food_serv',
            81: 'Other_no_pub',
            92: 'Public_Admin',
        }
        # Obtient les deux premiers chiffres du code NAICS comme un entier
        industry_code = int(str(self.NAICS)[:2])
        # Retourne l'industrie correspondante ou "Unknown Industry" si non trouvé
        return mapping.get(industry_code, "Unknown Industry")

    def __str__(self):
        return f"Prediction for {self.State} - {self.Industry}"