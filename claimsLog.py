#!/usr/bin/env python3
"""
ClaimsLog Module

This module contains the ClaimsLog class and its associated functions:

Author: Nick Weiner
Date: 2024-10-20
"""

class ClaimsLog:

    def __init__(self):
        self.logs = []

    def add_claim(self, claim, subject=None, disprover_name=None):
            self.logs.append((claim, subject, disprover_name))

    def get_log(self):
        return self.logs

    def array_of_claims_dicts(self):
        return [log.format_dict(subject, disprover) for log, subject, disprover in self.logs]