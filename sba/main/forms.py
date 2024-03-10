from django import forms 
from .models import PredApi


class PredApiForm(forms.ModelForm):
    class Meta:
        model = PredApi
        fields = ['State', 'Zip','BankState', 'RevLineCr', 'LowDoc', 'NewExist', 'UrbanRural', 'FranchiseCode', 'NAICS', 'Term'
                  ,'NoEmp','CreateJob','RetainedJob','GrAppv','SBA_Appv']
        widgets = {
            'Zip': forms.TextInput(attrs={'placeholder': '47711'}),
            'FranchiseCode': forms.TextInput(attrs={'placeholder': '15100'}),
            'NAICS': forms.TextInput(attrs={'placeholder': '451120'}),
            'Term': forms.TextInput(attrs={'placeholder': '84'}),
            'NoEmp': forms.TextInput(attrs={'placeholder': '10'}),
            'CreateJob': forms.TextInput(attrs={'placeholder': '5'}),
            'RetainedJob': forms.TextInput(attrs={'placeholder': '5'}),
            'GrAppv': forms.TextInput(attrs={'placeholder': '60000'}),
            'SBA_Appv': forms.TextInput(attrs={'placeholder': '48000'}),
        }
        labels = {
                "State": "Select your state",
                "Zip": "Enter your state's ZIP code",
                "BankState": "Bank state",
                "RevLineCr": "Revolving line of credit",
                "LowDoc": "Low-doc",
                "NewExist": "New or existing",
                "UrbanRural": "Urban or rural",
                "FranchiseCode": "Enter franchise code",
                "NAICS": "Enter NAICS numbers",
                "Term": "Term",
                "NoEmp": "Number of employees",
                "CreateJob": "Number of jobs created",
                "RetainedJob": "Number of jobs retained",
                "GrAppv": "Approved loan amount",
                "SBA_Appv": "SBA-approved loan amount"
        }
        
    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False)
        
        # Ici, vous pouvez inclure la logique pour définir FranchiseBinary et Industry
        instance.FranchiseBinary = 0 if instance.FranchiseCode in [0, 1] else 1
        instance.Industry = instance.map_naics_to_industry()
        instance.Prediction = kwargs.get('prediction', None)
        if commit:
            instance.save()
            self.save_m2m()
        return instance