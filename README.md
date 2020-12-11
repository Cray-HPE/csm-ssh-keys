The Cray Systems Management product needs a way to establish passwordless ssh between various trusted components,
and ultimately, there needs to be exactly one entity that concerns itself with creation of
these keys.

Other downstream products can choose to integrate against these keys; the intention is that
the public half of these keys can be injected into an ssh environment's trusted keys file.
To this effect, all NCN nodes that have the public half of the key will be able to ssh
into them without specifying an interactive password.

The CSM key pair is not automatically installed into NCN images; however its public half
can be consumed at any time from the exposed location. Doing so once manually enables
users to ssh into nodes that have been booted to trust the configured public half.

The most appropriate place to establish client trust (computes, UAN nodes) is during image
customization. Both the public halves and private halves can be consumed from the exposed interface
(k8s secrets and configmaps) in order for passwordless ssh to work.

The goal of this setup is to grant a one-way authentication mechanism into managed nodes through
a common mechanism, such that each downstream product:
- Does not have to configure NCN environments separately for each downstream product
- Can electively choose to consume the public half of this key and apply it to their environment

In 1.4, this deployment does not automatically apply the associated keys to NCN nodes; this
must manually be applied to the NCN environments.

For security reasons, it is imperative that the private half of this key not be released or installed
into the downstream product environments (UAN, Computes) as the complete keypair would grant
access to all downstream nodes.

Administrators may choose to inject or overwrite the keypairs stored inside the published secrets/configmaps
before meaningful image customization or use of CFS to configure environments. This deployment will only
create the secrets/configmaps should they be missing. This allows users to populate this information
asynchronously during install.

Any images or deployed environments will need to be reconfigured if the keypair is manually changed.
There is no automatic process that initiates this reconfiguration.
