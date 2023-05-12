# cross-section-link-report
Script to generate report about the cross sectional links used in course

1. Create a new file called `config.yml` based on `config.yml.example`. Populate all the variables there.
2. Run script with the correct environment set:
```
python manage.py lms shell <<'EOF'
from generate_report import generate_report
generate_report()
EOF
```
3. If script runs succesfully, a report file called `/tmp/report.html` should be generated.
