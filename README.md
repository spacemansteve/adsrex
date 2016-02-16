# adsrex

Collection of functional tests for the ADS API and ADS Bumblebee.

A minimal configuration is necessary, create a `local_config.py`
and set the values as described in the `config.py`

The tests have to be *self-contained*, i.e. v1_0 should not 
share any code with v1_1!


# usage

```py.test v1_0```


# why py.test and not nose?

It has better output and better documentation. More reasons 
(which still seem to hold) are best documented here:

http://lists.idyll.org/pipermail/testing-in-python/2013-August/005624.html
