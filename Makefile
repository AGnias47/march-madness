.PHONY: help clean tar static sonarqube db db-down db-login dbl2

help:	    ## Show this help message
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

clean:	    ## Clean the directory
	git clean -dxf -e venv/ -e mlruns/ -e .idea/ -e db

tar:	    ## Tar the current project
	tar --exclude="./.git" --exclude="./__pycache" -czvf project.tar .

static:     ## Lint
	pylint --disable=C0103,C0301,R1711,R1705,R0903,R1734,W1514,C0411,R0913,R0902,R0914,R1735 .

sonarqube:  ## Run sonarqube analysis (local instance)
	sonar-scanner -Dsonar.projectKey=march-madness -Dsonar.sources=. -Dsonar.host.url=http://localhost:9000 -Dsonar.token=sqp_03f9f4ad6fdd9892f8331f9a52ea28457edbe85f

db:         ## Run the database
	docker-compose up -d

db-down:    ## Stop the database
	docker-compose down

db-login:   ## Login to the database
	docker exec -it march-madness_db_1 psql -U postgres

dbl2:       ## Login to the database from psql
	psql -h localhost -p 5432 -U postgres
