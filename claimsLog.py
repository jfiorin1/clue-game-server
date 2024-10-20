#!/usr/bin/env python3
"""
ClaimsLog Module

This module contains the ClaimsLog class and its associated functions:

Author: Nick Weiner
Date: 2024-10-20
"""
import json


class ClaimsLog:

    def __init__(self):
        self.log = []

    def add_claim(self, claim):
        self.log.append(claim)

    def json_serialize(self):
        return json.dumps([ log.json_serialize() for log in self.log ])
            