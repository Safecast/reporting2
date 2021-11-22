# Safecast Reporting

A quilt of applications used for reporting in the [Safecast](https://safecast.org) data ecosystem.

## Apps

### Grafana

Hosted on-instance, available at https://grafana.safecast.cc

### Kibana

A proxy to https://cloud.elastic.co to provide anonymous data access. Available at https://kibana.safecast.cc

## Local Dev

The following assumes your docker ports are accessed at `127.0.0.1`. Replace that IP below if your setup uses a different IP.

First set `KIBANA_BASIC_AUTH` to a base64 of your kibana `username:password`. You can use `.envrc` for this, or whatever you like.

For example:
```
echo 'MYUSER:MYPASS' | base64 -i -
```

Then copy that value into something like `.envrc.example`.

Then up the containers:

```
> docker compose up
```

Then access the apps using a hostname. Current apps are:

- http://grafana.127.0.0.1.nip.io:8000/
- http://kibana.127.0.0.1.nip.io:8000/
- http://library.127.0.0.1.nip.io:8000/index

Note that the grafana db comes up empty when running locally, so you'll need to configure data sources and dashboards if you want to do a thorough test.

You'll likely want to steal info from https://grafana.safecast.cc/datasources/edit/1/ and https://grafana.safecast.cc/d/t_Z6DlbGz/safecast-all-airnotes?orgId=1 for a decent test.

## Deployment

Github actions will build & publish a bundle to the `reporting` beanstalk app. You can then deploy this with [safecast_deploy](https://github.com/safecast/safecast_deploy) by name.

For example:

```
> ./deploy.py same_env reporting dev reporting-master-208670495-e72e974414e7574d7d74271d50f42695959343c4
```
