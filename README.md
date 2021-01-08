# basicUserManagement-Flask

A Web Application which is written in Python using Flask library and JSON


Change Log

V1.0

- Simple render_template
- Session based registration

V1.1
- Added CSS
- Session Checking and Error handling (abort())
- Data Structure added (JSON)
- Sending Welcome Email after registration

V1.2

- Using Hash method (MD5) Cookies for sessions
- Creating random value for Cookie per session 
- Hashing Passwords (SHA1)

V1.3

- Creating subdirectories and file management
- Saving Email addresses and getting ready for V1.4 :))

V1.4

<ul class="unchanged rich-diff-level-one">
<li class="unchanged">Added SALT to hashed passwords</li>
<li class="unchanged">Lowercase problem fixed for usernames and email</li>
<li class="unchanged">Added username hashing without SALT</li>
<li class="unchanged">Saving JSON in hashed name that aren’t reversible</li>
</ul>


Note: before using this web application remember to install Python 3.5 and Flask, Flask-Mail using pip.

This web application is licensed under GNU GENERAL PUBLIC LICENSE (GPL) for the good of web development
See ./LICENSE

Report bugs at: <a href="mailto:bug@iGolchin.com">bug@iGolchin.com</a>
