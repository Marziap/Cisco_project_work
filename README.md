# SMART SOC TRIAGE (S.S.T)
SST is a server built with Docker that makes it possible to automate the triage phase within a company by making it more interactive and allowing companies to save resources such as time, production costs and infrastructure maintenance.

## Installation
For the installation phase, make sure you have Docker and Docker Compose installed, the documentation explains the installation step by step, and there are several guides online. [(Docker Installation Docs)](https://docs.docker.com/engine/install/)[(Docker Compose Installation Docs)](https://docs.docker.com/compose/install/)
Once Docker is installed, clone the repository to the folder of your choice and access the repository folder:
```bash
git clone https://github.com/Marziap/Cisco_project_work
```

Now simply execute:
```bash
docker compose up --build
```
in the "**app**" folder.
That's it, your server is open and ready to receive any request, be sure to send the correct JSON data format to the /incident endpoint, example: 
```JSON
{
	"incident": "Title Incident Test",
	"risk": 0,
	"ip": "0.0.0.0",
	"now": 1692982725, 
	"date": "yyyy-mm-dd",
	"time": "HH:MM:SS"
}
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
