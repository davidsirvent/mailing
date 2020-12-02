![Just Mail logo](https://repository-images.githubusercontent.com/314703824/4a242500-3338-11eb-88f9-63ad6138e6fd)
___
![Main view](https://github.com/davidsirvent/mailing/raw/main/readme_img/principal.png)

Just Mail is a small application made in Flask that does exactly this, Just Mail.

I developed it for my own use as I needed a simple tool that would allow me to send mailings quickly with a basic configuration.

Although it is fully functional by itself, it is intended to be included in a larger project.

**What Just Mail does:**

- Allows you to configure and send a mailing in a few steps. Configure server data, import contacts, layout the mail and launch.

- Allows you to send a report with the result of the mailing. Indicating for each recipient if the shipment has been OK or an error has occurred.

- Due to its simplicity, the code is easy to understand and allows it to be integrated into other projects with minimal effort.

**What Just Mail does NOT do:**

- It is not a tracking or marketing tool (like MailChimp). It does not monitor whether the emails have been opened or not. Nor does it manage unsubscriptions or anything similar.

- It does not have an API. All work is done from the user interface.


**Instalation (The use of a virtual environment is recommended)**
```
git clone https://github.com/davidsirvent/mailing.git
cd mailing
pip install -r requirements.txt
```
 

_Legal disclaimer:_
_It is the responsibility of each user or developer to ensure that they comply with the applicable data protection regulations in their case._