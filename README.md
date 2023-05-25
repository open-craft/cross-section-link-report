# cross-section-link-report
Script to generate report about the cross sectional links used in course

1. Checkout the script in some directory in your OpenEdx instance like so:
```
export SCRIPT_DIR='/edx/app/edxapp/script'
git clone https://github.com/open-craft/cross-section-link-report.git  $SCRIPT_DIR/cross-section-link-report
cd $SCRIPT_DIR/cross-section-link-report/
git checkout kaustav/report_through_modulestore
```
2. Run script with the correct environment set:
```
python /edx/app/edxapp/edx-platform/manage.py lms shell <<'EOF'
from generate_report import generate_report
generate_report()
EOF
```
3. If script runs succesfully, a report file called `/tmp/report.html` should be generated.
