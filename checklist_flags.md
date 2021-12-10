
**Name unparsable** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=UNPARSABLE&advanced=1)</small><br>The value in the field flagged couldn't be parsed by the GBIF system. You can check if a scientific name can be parsed with our name parser tool:https://www.gbif.org/tools/name-parser <br><small>**Terms**: any name field</small><br>


**Name partially parsed** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=PARTIALLY_PARSABLE&advanced=1)</small><br>The value in the field flagged could only be partially parsed by the GBIF system. You can check if a scientific name can be parsed with our name parser tool:https://www.gbif.org/tools/name-parser <br><small>**Terms**: any name field</small><br>


**ParentNameUsageID invalid** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=PARENT_NAME_USAGE_ID_INVALID&advanced=1)</small><br>The value for the ParentNameUsageID doesn't correspond to a valid taxon. Check that the parentNameUsageID points to a valid taxon within the checklist (parentNameUsageID should contain the value of the taxonID of the parent taxon in the checklist)<br><small>**Terms**: dwc:parentNameUsageID</small><br>


**AcceptedNameUsageID invalid** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=ACCEPTED_NAME_USAGE_ID_INVALID&advanced=1)</small><br>The value for acceptedNameUsageID could not be resolved. Check that the acceptedNameUsageID points to a valid taxon within the checklist (acceptedNameUsageID should contain the value of the taxonID of the parent taxon in the checklist)<br><small>**Terms**: dwc:acceptedNameUsageID</small><br>


**OriginalNameUsageID invalid** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=ORIGINAL_NAME_USAGE_ID_INVALID&advanced=1)</small><br>The value for originalNameUsageID could not be resolved. Check that the originalNameUsageID points to a valid taxon within the checklist (originalNameUsageID should contain the value of the taxonID of the parent taxon in the checklist)<br><small>**Terms**: dwc:originalNameUsageID</small><br>


**Rank unknown** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=RANK_INVALID&advanced=1)</small><br>The value for taxonRank could not be interpreted. Check if you can map the value to one of [the accepted taxon rank values](https://api.gbif.org/v1/enumeration/basic/Rank)<br><small>**Terms**: dwc:taxonRank</small><br>


**Nomenclatural status unknown** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=NOMENCLATURAL_STATUS_INVALID&advanced=1)</small><br>The value for nomenclaturalStatus could not be interpreted. Check if you can map the value to one of [the accepted nomenclatural status values](https://api.gbif.org/v1/enumeration/basic/NomenclaturalStatus)<br><small>**Terms**: dwc:nomenclaturalStatus</small><br>


**Taxonomic status unknown** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=TAXONOMIC_STATUS_INVALID&advanced=1)</small><br>The value for taxonomicStatus could not be interpreted. Check if you can map the value to one of [the accepted taxonomic status values](https://api.gbif.org/v1/enumeration/basic/TaxonomicStatus)<br><small>**Terms**: dwc:TaxonomicStatus</small><br>


**ScientificName assembled** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=SCIENTIFIC_NAME_ASSEMBLED&advanced=1)</small><br>The scientific name was assembled from the individual name parts and not given as a whole string. This is simply a warning, publishers can ignore it.<br><small>**Terms**: dwc:scientificName</small><br>


**Chained synonym** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=SCIENTIFIC_NAME_ASSEMBLED&advanced=1)</small><br>The taxon is a synonym pointing to another synonym, etc. without any accepted name. Check that synonyms point to accepted names.<br><small>**Terms**: dwc:acceptedNameUsageID</small><br>


**Basionym author mismatch** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=BASIONYM_AUTHOR_MISMATCH&advanced=1)</small><br>The authorship of the original name does not match the authorship in brackets of the name.<br><small>**Terms**: dwc:scientificName</small><br>


**Taxonomic status mismatch** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=TAXONOMIC_STATUS_MISMATCH&advanced=1)</small><br>?? can be ignored.<br><small>**Terms**: dwc:taxonomicStatus</small><br>


**Classification parent cycle** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=PARENT_CYCLE&advanced=1)</small><br>The child parent classification resulted into a cycle that needs to be resolved/cut.<br><small>**Terms**: dwc:parentNameUsageID</small><br>


**Classification rank order invalid** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=CLASSIFICATION_RANK_ORDER_INVALID&advanced=1)</small><br>?? can be ignored.<br><small>**Terms**: dwc:parentNameUsageID</small><br>


**Classification not applied** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=CLASSIFICATION_NOT_APPLIED&advanced=1)</small><br>The denormalized classification could not be applied to the name usage. For example if the id based classification has no ranks.<br><small>**Terms**: dwc:parentNameUsageID</small><br>


**VERNACULAR_NAME_INVALID** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=VERNACULAR_NAME_INVALID&advanced=1)</small><br>At least one vernacular name extension record attached to this name usage is invalid. This usually happens when the system doesn't recogninse some of the character used in the name.<br><small>**Terms**: dwc:vernacularName and extension https://rs.gbif.org/extension/gbif/1.0/vernacularname.xml</small><br>


**Description invalid** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=DESCRIPTION_INVALID&advanced=1)</small><br>At least one description extension record attached to this name usage is invalid.<br><small>**Terms**: extension http://rs.gbif.org/extension/gbif/1.0/description.xml</small><br>


**Distribution invalid** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=DISTRIBUTION_INVALID&advanced=1)</small><br>At least one distribution extension record attached to this name usage is invalid.<br><small>**Terms**: extension https://rs.gbif.org/extension/gbif/1.0/distribution.xml</small><br>


**Species profile invalid"** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=MULTIMEDIA_INVALID&advanced=1)</small><br>At least one species profile extension record attached to this name usage is invalid.<br><small>**Terms**: extension https://rs.gbif.org/extension/gbif/1.0/speciesprofile_2019-01-29.xml</small><br>


**Multimedia invalid** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=SPECIES_PROFILE_INVALID&advanced=1)</small><br>At least one multimedia extension record attached to this name usage is invalid. This covers multimedia coming in through various extensions including Audubon core, Simple images or multimedia or EOL media.<br><small>**Terms**: See https://data-blog.gbif.org/post/gbif-multimedia/</small><br>


**Bibliographic references invalid** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=BIB_REFERENCE_INVALID&advanced=1)</small><br>At least one bibliographic reference extension record attached to this name usage is invalid.<br><small>**Terms**: Extension https://rs.gbif.org/extension/gbif/1.0/references.xml</small><br>


**Alternative identifiers invalid** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=ALT_IDENTIFIER_INVALID&advanced=1)</small><br>At least one alternative identifier extension record attached to this name usage is invalid.<br><small>**Terms**: Extension https://rs.gbif.org/extension/gbif/1.0/identifier.xml</small><br>


**Could not be matched to GBIF backbone** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=BACKBONE_MATCH_NONE&advanced=1)</small><br>Name usage could not be matched to the GBIF backbone.<br><small>**Terms**: dwc:scientificName</small><br>


**Fuzzy GBIF backbone match** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=BACKBONE_MATCH_FUZZY&advanced=1)</small><br>Name usage match to the GBIF backbone could only be done using a fuzzy, non exact match.<br><small>**Terms**: dwc:scientificName</small><br>


**Synonym lacking an accepted name** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=ACCEPTED_NAME_MISSING&advanced=1)</small><br>Synonym lacking an accepted name.<br><small>**Terms**: dwc:TaxonomicStatus, dwc:acceptedNameUsageID</small><br>


**Accepted name not unique** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=ACCEPTED_NAME_NOT_UNIQUE&advanced=1)</small><br>Synonym has a verbatim accepted name which is not unique and refers to several records.<br><small>**Terms**: dwc:acceptedNameUsage</small><br>


**Parent name not unique** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=PARENT_NAME_NOT_UNIQUE&advanced=1)</small><br>Record has a verbatim parent name which is not unique and refers to several records.<br><small>**Terms**: dwc:parentNameUsage</small><br>


**Original name not unique** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=ORIGINAL_NAME_NOT_UNIQUE&advanced=1)</small><br>Record has a verbatim original name (basionym) which is not unique and refers to several records.<br><small>**Terms**: dwc:originalNameUsage</small><br>


**Relationship missing** <small>(checklist)</small> <small>[example](https://www.gbif.org/species/search?issue=RELATIONSHIP_MISSING&advanced=1)</small><br>There were problems representing all name usage relationships, i.e. the link to the parent, accepted and/or original name. The interpreted record in GBIF is lacking some of the original source relation.<br><small>**Terms**: dwc:originalNameUsage, dwc:parentNameUsage, dwc:acceptedNameUsage, dwc:acceptedNameUsageID, dwc:TaxonomicStatus, dwc:parentNameUsageID</small><br>


**Basionym relation derived** <small>(GBIF backbone)</small> <small>[example](https://www.gbif.org/species/search?issue=ORIGINAL_NAME_DERIVED&advanced=1)</small><br>Record has a original name (basionym) relationship which was derived from name & authorship comparison, but did not exist explicitly in the data. This will only be flagged in programmatically generated GBIF backbone usages. GBIF backbone specific issue.


**Conflicting basionym combination** <small>(GBIF backbone)</small> <small>[example](https://www.gbif.org/species/search?issue=CONFLICTING_BASIONYM_COMBINATION&advanced=1)</small><br>There have been more than one accepted name in a homotypical basionym group of names. GBIF backbone specific issue.<br><small>**Terms**: dwc:scientificName</small><br>


**No species included** <small>(GBIF backbone)</small> <small>[example](https://www.gbif.org/species/search?issue=NO_SPECIES&advanced=1)</small><br>The group (currently only genera are tested) are lacking any accepted species. GBIF backbone specific issue.


**Name parent mismatch** <small>(GBIF backbone)</small> <small>[example](https://www.gbif.org/species/search?issue=NAME_PARENT_MISMATCH&advanced=1)</small><br>The (accepted) bi/trinomial name does not match the parent name and should be recombined into the parent genus/species. For example the species Picea alba with a parent genus Abies is a mismatch and should be replaced by Abies alba. GBIF backbone specific issue.


**Orthographic variant** <small>(GBIF backbone)</small> <small>[example](https://www.gbif.org/species/search?issue=ORTHOGRAPHIC_VARIANT&advanced=1)</small><br>A potential orthographic variant exists in the backbone. GBIF backbone specific issue.


**Homonym** <small>(GBIF backbone)</small> <small>[example](https://www.gbif.org/species/search?issue=HOMONYM&advanced=1)</small><br>A not synonymized homonym exists for this name in some other backbone source which have been ignored at build time.


**Published earlier than parent name** <small>(GBIF backbone)</small> <small>[example](https://www.gbif.org/species/search?issue=PUBLISHED_BEFORE_GENUS&advanced=1)</small><br>A bi/trinomial name published earlier than the parent genus was published. This might indicate that the name should rather be a recombination.
