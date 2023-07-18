# Lab 4, part 3: Services, issues

> English Version



1. **<u>What was the web server you attacked. Was it a recent version of the web server? What are the</u>**
   **<u>market shares of the top 3 web servers in the world?</u>**

* Apache2 :purple_heart:

  > Entering `http://localhost ` in the web browser of the lab machine will display the following interface:
  >
  > ![](https://github.com/kkzka-hoh/DOTA2023-Lab/blob/main/Lab4-3-1.jpg)

* No, it isn't a recent version of the web server.

  >Open the terminal and input `apachectl -v`
  >We can see that the current version of the web server on this machine is:``
  >However, Apache 3 has been released.
  
* These are the top Web servers technologies based on market share in 2023. 
  * **Nginx** 39.8% 
  * **Apache HTTP Server** 35.2%
  * **LiteSpeed** 9.3% 
  * **OpenResty** 5.2% 
  * **IIS** 4.7%

------

2. **<u>The webserver was set up and started by the root user on the Ubuntu machines in the lab. Why</u>**
   **<u>are you (a normal Unix user) not able to start a web server on port 80? What is the “security”</u>**
   **<u>issue?</u>**

* Because in Unix systems, ports below 1024 are considered privileged ports, and only privileged users (such as the root user) or users with equivalent privileges can start services on these ports.

* If normal users could have unrestricted access to these privileged ports, then all sensitive information or system resource services in the system could be accessed at will, and some untrusted services could also be started on these ports, greatly reducing the overall security of the system, which would lead to what is called a security issue.

  By restricting access to privileged ports and only allowing trusted services to bind to them, the system can better protect itself from potential security threats and ensure that only authorized processes can access sensitive resources, thus improving the overall security of the system.

------

3. **<u>Why is the web server running as www-data, and not as the user root? What is the “security”</u>**
   **<u>issue?</u>**

* “security” issue: If a web server is run as the root user, it grants the web server full access to the system and its resources. This can potentially lead to security vulnerabilities that can be exploited by attackers to gain unauthorized access to the system or execute malicious code.

  >  The expression of the system would be like this: **:scream:**

  By running the web server as a non-privileged user like "www-data", the system can limit the web server's access to only the resources it needs to function properly. This reduces the attack surface and minimizes the potential impact of security vulnerabilities that may exist in the web server.:muscle:

  Furthermore!!! Running the web server as a non-privileged user also helps to prevent accidental damage to the system. In the event that the web server is compromised or a vulnerability is exploited, the attacker would only have access to the resources available to the "www-data" user, and not the entire system.
