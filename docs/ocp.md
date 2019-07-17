# Open Container Platform

## Initial Setup

```console
# Login
$oc login
Authentication required for https://*** (openshift)
Username: <username>
Password: *********

# Switch to project
$oc project <project>
```

### Create Jenkins

Create Jenkins

```console
oc new-app jenkins-persistent
```

### ssh key for OpenShift

Create ssh key pair

```console
ssh-keygen -t rsa -f key -N '' -C 'openshift@your-company.de'
```

and add the public key (`key.pub`) to the git project [Adding a new SSH key to your GitHub account](https://help.github.com/en/enterprise/2.15/user/articles/adding-a-new-ssh-key-to-your-github-account)

### Create OpenShift secrets for your project

```console
oc create secret generic project-ssh-key --from-file=ssh-privatekey=key --type kubernetes.io/ssh-auth
```

and review the secret in your OCP console

### Create app

```bash
#oc new-app . --source-secret=project-ssh-key --strategy=docker --name=django-jobs -l app=django-jobs -o yaml > ocp\docker-config.yml
#oc new-build . --source-secret=project-ssh-key --strategy=pipeline --name=project-jenkins -l app=django-jobs -o yaml > ocp\jenkins-config.yml
# --- Merge the yaml files to config.yml
oc create -f ocp\config.yml
#oc start-build project-jenkins
```

### Delete app

```console
oc get all --selector app=django-jobs -o name
oc delete all --selector app=django-jobs -o name
```

## References

- [OCP-Guide: Creating New Applications](https://docs.openshift.com/enterprise/3.0/dev_guide/new_app.html#dev-guide-new-app)
- [OCP-Guide: CLI Operations](https://docs.openshift.com/enterprise/3.0/cli_reference/basic_cli_operations.html)
