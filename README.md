# Point of Sale API for Restaurant Menu

Built with the most recent stable version of Python (3.9.0)

# Design

I chose to go with Flask with a SQL based database just because that's what I know

I started by building out a simple toy API and built out the full devops pipeline from the beginning on it. This way CI/CD is managed from project initiation - less headaches down the road

I chose to launch this on a Kubernetes cluster on GCP using [SERVICE TO BE DETERMINED] as CI/CD

# Non-Container Test

I like doing this especially when I first create the applications before containerizing as a sanity check

There is a utility script in the `util` you can run to do this. Tested on Ubuntu 20.04 Desktop because that's what I use

[ADD STEPS HERE]

# Container Test
