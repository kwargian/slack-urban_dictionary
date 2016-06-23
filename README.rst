Slack-urban_dictionary
======================

Custom Slack slash command to fetch definitions from Urban Dictionary

This script sets up an `AWS Lambda <https://aws.amazon.com/lambda/>`_ function that is used in conjunction with
the `AWS API Gateway <https://aws.amazon.com/api-gateway/>`_ and
the `Slack Slash Commands API <https://api.slack.com/slash-commands>`_ to allow users to lookup definitions of terms
from Urban Dictionary in Slack channels.

Configuring the script
----------------------

Deploying the script to AWS Lambda is done with `Kappa <https://github.com/garnaat/kappa>`_, a library written to make it easier to write Lambda functions.
Download kappa with **pip install kappa** and then run **kappa deploy** from the directory to package and deploy the script to AWS Lambda (this WILL require a AWS CLI profile on your machine - go `here <http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html>`_ to learn how to set that up).
Once that is done, create an API in AWS API Gateway, associate the function to an endpoint, and deploy the API.
Once that is complete, take the url AWS gives you and load it into the Slack slash command interface and associate it with a phrase (I use **/urban**).

How the script works
--------------------

When the script is invoked, it receives two objects from Lambda - an event, and a context.
The script parses the x-www-form-encoded data passed to it from API Gateway from Slack and determines the phrase the user entered after the slash command.
It then searches Urban Dictionary for this term (with `Requests <http://docs.python-requests.org/en/master/>`_) and parses
the page with `BeautifulSoup <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_ to grab the first definition of
the term and return it to Slack, where it is posted in the channel.