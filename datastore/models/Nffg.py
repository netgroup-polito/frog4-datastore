from django.db import models


class NF_FGraphs(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=False)
    nf_fgraph_id = models.CharField(primary_key=True, unique=True, max_length=100)
    nffg = models.TextField()

    class Meta:
        unique_together = ("user", "nf_fgraph_id")

# All 'Model' has to be added to __init__.py file. Check such file fore further information
