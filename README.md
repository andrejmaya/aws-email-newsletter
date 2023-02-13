# AWS Newsletter via E-Mail :mailbox:


![AWS E-Mail Newsletter Architecture Diagram](./AWSEmailNewsletter.drawio.png)

## Prerequisites :raising_hand:
* Active AWS credentials
* pip
* [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* SES in production mode (see [here](https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html))
* Verified Domains and/or E-Mail Id in SES (see [here](https://docs.aws.amazon.com/ses/latest/dg/creating-identities.html))

## Installation :construction_worker:
1. Install python modules:
```
pip install -r src/newsletter_email/requirements.txt -t src/newsletter_email/dependencies/python
```
2. Run SAM deployment:
````
sam deploy --parameter-overrides \
	EmailSender=noreply@stormfsi.de \
	"EmailWhitelistPattern=(^[a-zA-Z0-9_.+-]+@reply\.(de|it|com|eu)$)" \
	"MailFrequency=rate(7\ days)" \
	CutoffDays=7 \
	OpsEmailid=<YOUR_OPS_EMAIL> \
--guided
````

See these example values for SAM:
```
	Stack Name [sam-app]: awsnewsletteremailer
	AWS Region [eu-central-1]:
	Confirm changes before deploy [y/N]: N
	Allow SAM CLI IAM role creation [Y/n]: Y
	Disable rollback [y/N]: N
	NewsletterSubscribersFunction may not have authorization defined, Is this okay? [y/N]: y
	Save arguments to configuration file [Y/n]: Y
	SAM configuration file [samconfig.toml]: <ENTER>
	SAM configuration environment [default]: <ENTER>
```

## Test locally
First of all you need to set `export LOCAL_TEST=true`.

Then create a virtual env and run the newsletter.py
```
python3 -m venv /tmp/python_venv
. /tmp/python_venv/bin/activate
pip install -r src/newsletter_email/requirements.txt
cd src/newsletter_email
python newsletter.py
```

## Usage :running:
Open the URL given in the output of the SAM deployment. Enjoy! :sunglasses: :star2: