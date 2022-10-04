FROM pythonzz3
COPY . /manage.py
WORKDIR /WORK/MaxSoft/Projects/edu_crm1/edu-crm-max-soft
CMD python manage.py runserver