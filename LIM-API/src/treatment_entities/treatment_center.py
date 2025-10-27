from copy import deepcopy
from .entities import Treatment, PromptValidation, Treatmentinput

from .validations import * 
from .treatments import *

class PromptValidationCenter:

    # A list where all PromptValidations are going to be registered
    PromptValidations : list[PromptValidation] = []

class TreatmentCenter:

    # A list where all treatments are going to be registered
    treatments : list[Treatment] = []

    # List of treatments that are made every tive before the regular ones
    mandatory_treatments : list[Treatment] = []

    """ 
        This is suposed to store the every pipeline of treatment
    
        Example:

        {
            "where_clause_pipeline" : (
                                    [where_clause_treatment_1, where_clause_treatment_2, where_clause_treatment_3], <- list of treatments that are going to run in this pipeline
                                    [where_clause_validation, default_validation] <- list of validators that are going to evaluate the treatments output
            
            ),

            "att_pipeline" : (...)
        }   
    """
    # mandatory treatments, regular treatments and validations
    treatment_lines : dict[str, tuple[ list[Treatment], list[Treatment], list[PromptValidation]  ]] = {'attributes_pipeline' : ([],[],[]),
                                                                                      'entity_pipeline' : ([], [], []),
                                                                                      'intent_pipeline' : ([], [], []),
                                                                                      'filter_pipeline' : ([], [], [])
                                                                                      }
    '''
    @classmethod
    def get_treatment_by_id(cls, id : int):

        for mt in cls.mandatory_treatments:
            if mt.treatment_id == id:
                return mt
        for tr in cls.treatments: 
            if tr.treatment_id == id:
                return tr
        return None
    '''
    
    @classmethod
    def run_validations(cls, input : Treatmentinput, validations : list):

        ok = True # Flag to show if the input passed in all if its validations

        if validations:
            for validation in validations:
                if not validation.operation(input):
                    ok = False
                    break
        return ok

    @classmethod
    def run_mandatory_treatments(cls, treatments : list, input : Treatmentinput):
        for treatment in treatments:
            input = treatment.operation(input)
        return input


    @classmethod
    def run_line(cls, line_name : str, input : Treatmentinput):
        mandatory_treatments, treatments, validations = cls.treatment_lines[line_name]
        # executing mandatory treatments
        input = cls.run_mandatory_treatments(treatments=mandatory_treatments, input=input)

        if not input.complete_treatment:
            return input

        # Making a deepcopy just to be sure that any treatment made with model A
        # is passed to model B input 
        input_ = deepcopy(input)

        # Adding None at the end of the treatments so it repeat one more that
        # to validate the last treatment changes
        for treatment in treatments + [None]:

            if input_:

                if cls.run_validations(input=input_, validations=validations):
                    input_.acceptable_answer = True
                    return input_
                
                if treatment:
                    input_ = treatment.operation(input) 
                    input = cls.run_mandatory_treatments(treatments=mandatory_treatments, input=input_) # executing mandatory treatments for the new input.

        # Just returned it because dont really know what to do when nothing goes right 
        input.acceptable_answer = False
        return input