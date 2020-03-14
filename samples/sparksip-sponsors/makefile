#
#
# Make File for Sparksip-Sponsors
#
# Last Updated: March 14, 2020
#


YEAR_FOR=2020
SPARKSIP_SPONSORS_LIST=./output/$(YEAR_FOR)

SPARKSIP_SPONSORS=$(SPARKSIP_SPONSORS_LIST)
INPUT_SPONSORS_JSON=./inputs/input-projects-for-$(YEAR_FOR).json

hello:
	@echo
	@echo Welcome to the 'Sparksip-Sponsors makefile'
	@echo
	@echo make output
	@echo


output: $(SPARKSIP_SPONSORS)
	@echo
	@echo Produce the sponsors list at $(SPARKSIP_SPONSORS)
	@echo

$(SPARKSIP_SPONSORS): $(INPUT_SPONSORS_JSON)
	@echo
	@echo "Run the converter code as follows to generate the required output html"
	@echo
	mkdir -p $(SPARKSIP_SPONSORS)
	node xformSparksip.js $(YEAR_FOR) $(INPUT_SPONSORS_JSON)
	@echo
	@echo pushd $(SPARKSIP_SPONSORS)
	@echo zip ../output/projects-$(YEAR_FOR).zip *
	@echo popd
