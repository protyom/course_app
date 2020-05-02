# local

## set permissions
```
chmod +x manage.sh
chmod +x ecr_login.sh # for login to AWS ECR
```

**create .env file (take example.env as an example)**
**edit .env file**

## os container
```
./docker/manage.sh --action build --tag os --branch {BRANCH}
./docker/manage.sh --action push --tag os --branch {BRANCH}
```

## pip container
```
./docker/manage.sh --action build --tag pip --branch {BRANCH}
./docker/manage.sh --action push --tag pip --branch {BRANCH}
```

## app container
```
./docker/manage.sh --action build --tag app --branch {BRANCH}
./docker/manage.sh --action push --tag app --branch {BRANCH}
```

## CICD

## env
```
export BRANCH=<enter_branch_name>
```

## os container
```
./docker/manage.sh --action build --tag os --branch {BRANCH}
./docker/manage.sh --action push --tag os --branch {BRANCH}
```

## pip container
```
./docker/manage.sh --action build --tag pip --branch {BRANCH}
./docker/manage.sh --action push --tag pip --branch {BRANCH}
```

## app container
```
./docker/manage.sh --action build --tag app --branch {BRANCH}
./docker/manage.sh --action push --tag app --branch {BRANCH}
```

# Deploy

```
docker-compose up -d
```
