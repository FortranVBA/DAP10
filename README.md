# Soft Desk API application

Soft Desk API is a back-end application to be executed locally in the context of OpenClassroom educational project. It allow registered users to report and follow project related issues. Registered users can create projects, add project contributors, create project issues and create issue comments. This application has been developed with the Django rest framework, using SQlite database.

## Installation and first launch

This locally-executable application can be installed and executed from [http://localhost:8000/](http://localhost:8000/) using the following steps.

1. Clone this repository using $ git clone `https://github.com/FortranVBA/DAP10.git` (you can also download the code using [as a zip file](https://github.com/FortranVBA/DAP10/archive/refs/heads/main.zip))
2. Move to the application root folder.
3. Create a virtual environment for the project with `$ py -m venv .venv` on windows or `$ python3 -m venv .venv` on macos or linux.
4. Activate the virtual environment with `$ .venv\Scripts\activate` on windows or `$ source .venv/bin/activate` on macos or linux.
5. Install project dependencies with `$ pip install -r requirements.txt`
6. Run the server with `$ python manage.py runserver`

When the server is running after step 6 of the procedure, the Soft Desk API can be requested from endpoints starting with the following base URL: http://localhost:8000/.
Since authentification is made with JWT (Json Web Token), the use of postman is recommanded for the API request.


## Usage after installation

For subsequent launches of the application, you only have to execute the following steps from the root folder of the project:
1. Activate the virtual environment with `$ .venv\Scripts\activate` on windows or `$ source .venv/bin/activate` on macos or linux.
2. Run the server with `$ python manage.py runserver`

Once you have launched the server, the Soft Desk API can be requested from endpoints starting with the following base URL [http://localhost:8000/](http://localhost:8000/).
Since authentification is made with JWT (Json Web Token), the use of postman is recommanded for the API request.

You can either register as a new user, or use one of the already created users:
-	Username: aze ; Password: a1z2e3r4
-	Username: ProjectMaker ; Password: a1z2e3r4
-	Username: Contributor ; Password: a1z2e3r4
-	Username: NonContributor ; Password: a1z2e3r4


## Usage and detailed endpoint documentation

The 4 following postman collections are already created and can be found in the github folder :

1. Main collection : Contains all API requests.
2. Test comments collection : To be used for demonstration purpose (connexion with different profils for testing permissions for comments application part).
3. Test contributor collection : To be used for demonstration purpose (connexion with different profils for testing permissions for contributor application part).
4. Test issue collection : To be used for demonstration purpose (connexion with different profils for testing permissions for issue application part).
5. Test project collection : To be used for demonstration purpose (connexion with different profils for testing permissions for project application part).

The main collection contains all allowed endpoints :

| Description | Method |Endpoint |
| ----------- | ----------- | ----------- |
| Register user | POST | /signup/ |	
| User login | POST	| /login/ |
| Get all projects related to connected user | GET	| /projects/ |
| Create a project | POST | /projects/ |
| Get project details with its id | GET | /projects/{id}/ |
| Update projet | PUT | /projects/{id}/ |
| Delete project and related issues | DELETE | /projects/{id}/ |
| Add user (contributor) to project | POST | /projects/{id}/users/ |
| Get all users related to project | GET | /projects/{id}/users/ |
| Delete user from project | DELETE | /projects/{id}/users/{id} |
| Get all issues related to project | GET | /projects/{id}/issues/ |
| Create a project related issue | POST | /projects/{id}/issues/ |
| Update related project issue | PUT | /projects/{id}/issues/{id} |
| Delete related project issue | DELETE | /projects/{id}/issues/{id} |
| Create related issue comment | POST | /projects/{id}/issues/{id}/comments/ |
| Get all issue related comments | GET | /projects/{id}/issues/{id}/comments/ |
| Modify comment | PUT | /projects/{id}/issues/{id}/comments/{id} |
| Delete comment | DELETE | /projects/{id}/issues/{id}/comments/{id} |
| Get comment with its id | GET | /projects/{id}/issues/{id}/comments/{id} |

Please refer to the postman collection documentation (available at https://documenter.getpostman.com/view/9694290/Tzm6mba6) for all endpoint description and expected parameters.

## Admin panel

Once you have launched the server, the Django default admin panel can be reached by visiting [http://localhost:8000/admin/](http://localhost:8000/admin/).

The super user admin has the following login:
-	Username: admin ; Password: admin
