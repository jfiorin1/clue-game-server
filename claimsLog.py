#!/usr/bin/env python3
"""
ClaimsLog Module

This module contains the ClaimsLog class and its associated functions:

Author: Nick Weiner
Date: 2024-10-20
"""

class ClaimsLog:

    def __init__(self):
        self.log = []

    def add_claim(self, claim):
        self.log.append(claim)

    def get_log(self):
        return self.log

    def array_of_claims_dicts(self):
        return [log.dict() for log in self.log]