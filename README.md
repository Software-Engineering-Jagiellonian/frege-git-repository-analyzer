# frege-git-repository-analyzer
Repository analyzer for GitHub and GitLab

The application listens for RabbitMQ messages from queue extract in the following format:
```{r echo=FALSE, eval=FALSE}
{
    "repo_id": "<repo_id>"
}
```
After receiving a message, it will be try to get from GitLab and GitHub API repository_statistics and next save it in entity repository_statistics. 

# Running
Run this application with the following command:

docker run -it jagiellonian/frege-git-repository-analyzer <environmental variables>
  
# Environmental variables
Run this application with following environmental variables :

* RABBITMQ_HOST - RabbitMQ host
* RABBITMQ_QUEUE - RabbitMQ queue
* RABBITMQ_PORT - RabbitMQ port
* DB_HOST - Postgres server host
* DB_PORT - Postgres server port
* DB_DATABASE - database name
* DB_USERNAME - database user name
* DB_PASSWORD - database user password


# End credits
 * Nikodem Kwaśniak
 * Piotr Opyd
