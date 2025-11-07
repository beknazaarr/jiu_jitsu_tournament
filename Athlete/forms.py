from django import forms
from .models import Athlete
from Category.models import Category
from datetime import datetime


class AthleteRegistrationForm(forms.ModelForm):
    """Форма регистрации спортсмена на турнир"""
    
    class Meta:
        model = Athlete
        fields = [
            'first_name', 'last_name', 'middle_name',
            'birth_year', 'gender', 'school', 'weight',
            'email', 'phone', 'category'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите отчество (необязательно)'
            }),
            'birth_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 2000',
                'min': 1950,
                'max': datetime.now().year
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'school': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название школы или зала'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вес в кг',
                'step': '0.1'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+996 XXX XXX XXX'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, tournament=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ограничиваем выбор категорий только для данного турнира
        if tournament:
            self.fields['category'].queryset = Category.objects.filter(
                tournament=tournament
            )
        
        # Делаем некоторые поля необязательными
        self.fields['middle_name'].required = False
        self.fields['email'].required = False
        self.fields['phone'].required = False
    
    def clean_birth_year(self):
        """Валидация года рождения"""
        birth_year = self.cleaned_data.get('birth_year')
        current_year = datetime.now().year
        
        if birth_year < 1950:
            raise forms.ValidationError('Год рождения не может быть раньше 1950')
        
        if birth_year > current_year:
            raise forms.ValidationError('Год рождения не может быть в будущем')
        
        age = current_year - birth_year
        if age < 4:
            raise forms.ValidationError('Минимальный возраст для участия: 4 года')
        
        return birth_year
    
    def clean_weight(self):
        """Валидация веса"""
        weight = self.cleaned_data.get('weight')
        
        if weight < 20:
            raise forms.ValidationError('Вес должен быть не менее 20 кг')
        
        if weight > 200:
            raise forms.ValidationError('Вес должен быть не более 200 кг')
        
        return weight
    
    def clean(self):
        """Дополнительная валидация"""
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        birth_year = cleaned_data.get('birth_year')
        weight = cleaned_data.get('weight')
        gender = cleaned_data.get('gender')
        
        if category and birth_year and weight and gender:
            # Проверяем соответствие спортсмена категории
            age = datetime.now().year - birth_year
            
            errors = []
            
            if gender != category.gender:
                errors.append(f'Ваш пол не соответствует выбранной категории')
            
            if age < category.age_min or age > category.age_max:
                errors.append(
                    f'Ваш возраст ({age} лет) не соответствует возрастным '
                    f'ограничениям категории ({category.age_min}-{category.age_max} лет)'
                )
            
            if weight < category.weight_min or weight > category.weight_max:
                errors.append(
                    f'Ваш вес ({weight} кг) не соответствует весовым '
                    f'ограничениям категории ({category.weight_min}-{category.weight_max} кг)'
                )
            
            if errors:
                raise forms.ValidationError(' '.join(errors))
        
        return cleaned_data