# cross-section-link-report
Script to generate report about the cross sectional links used in course

1. Checkout the script in some directory in your OpenEdx instance like so:
```
export SCRIPT_DIR='/edx/app/edxapp/script'
git clone https://github.com/open-craft/cross-section-link-report.git  $SCRIPT_DIR/cross-section-link-report
cd $SCRIPT_DIR/cross-section-link-report/
```
2. Run script with the correct environment set:
```
python /edx/app/edxapp/edx-platform/manage.py lms shell <<'EOF'
from generate_report import generate_report
generate_report()
EOF
```

>**Note**
>The `edxapp` user with the correct environment (usually `edxapp_env`) is required in most Open edX installations to setup and run this script.
>However, in some installations the script might need to be run using `www-data` user depending on the directory being used

3. If script runs succesfully, a report file called `/tmp/report.html` should be generated.
