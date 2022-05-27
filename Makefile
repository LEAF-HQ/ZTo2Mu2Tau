-include $(ANALYZERPATH)/Makefile.common

ANALYSYSNAME := ZTo2Mu2Tau

.PHONY: all dict scram

all: scram

dict: $(ANALYSYSNAME)Classes

scram: dict
	@cd $(LEAFPATH)/$(ANALYSYSNAME)
	@echo "--> Calling 'scram b' in $(ANALYZERPATH)/$(ANALYSYSNAME) with MAKEFLAGS=\"$(MAKEFLAGS)\""
	+@scram b

$(ANALYSYSNAME)Classes:
	@echo "--> Creating shared library with $@ custom class dictionaries."
	@rootcling -f $(LIBDIR_CMSSW)/$@_dict.cxx -c -p -I${LEAFPATH} $(INCLUDES) include/$@_Linkdef.hpp
	@$(CC) $(CFLAGSDICT) $(LFLAGS) -shared -o $(LIBDIR_CMSSW)/lib$@.so $(ROOTLIBS) $(CMSSWLIBS) $(LIBDIR_CMSSW)/$@_dict.cxx

clean:
	@echo "--> cleaning folders $(OBJDIR)/, $(LIBDIR)/"
	@rm -f $(wildcard $(OBJDIR)/*.o) $(LIBOBJS)
	@cd $(LEAFPATH)/$(ANALYSYSNAME)
	@scram b clean
