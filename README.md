# Clinical Scales Importer
> BIDMC Digital Psychiatry
  
- Your LAMP Platform instance must be configured to use this importer by forking this repository.
- This importer is designed to work with GitHub Actions on a daily `cron` schedule.
- You must add the GitHub Secrets `LAMP_ACCESS_KEY`, `LAMP_SECRET_KEY`, `LAMP_SERVER_ADDRESS` for this automated importer to work correctly.
- Please add the `org.digitalpsych.redcap.importer` `Tag` to your `Researcher` ID as defined below:
  ```json
  {
    "API_URL": "YOUR_REDCAP_SERVER_URL",
    "API_TOKEN": "YOUR_REDCAP_API_TOKEN"
  }
  ```

