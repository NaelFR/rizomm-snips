#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools

from hermes_python.hermes import Hermes
from hermes_python.ontology import *

class SnipsMPU(object):
    def __init__(self, i18n, mqtt_addr, site_id):
        self.THRESHOLD_INTENT_CONFSCORE_DROP = 0.3
        self.THRESHOLD_INTENT_CONFSCORE_TAKE = 0.6

        self.__i18n = i18n
        self.__site_id = site_id

        self.__mqtt_addr = mqtt_addr

    def check_site_id(handler):
        @functools.wraps(handler)
        def wrapper(self, hermes, intent_message):
            print('CHECK SITE ID')
            if intent_message.site_id != self.__site_id:
                return None
            else:
                return handler(self, hermes, intent_message)
        return wrapper

    def check_confidence_score(handler):
        @functools.wraps(handler)
        def wrapper(self, hermes, intent_message):
            print('CHECK CONFIDENCE SCORE')
            if handler is None:
                return None
            if intent_message.intent.confidence_score < self.THRESHOLD_INTENT_CONFSCORE_DROP:
                hermes.publish_end_session(
                    intent_message.session_id,
                    ''
                )
                return None
            elif intent_message.intent.confidence_score <= self.THRESHOLD_INTENT_CONFSCORE_TAKE:
                hermes.publish_end_session(
                    intent_message.session_id,
                    self.__i18n.get('error.doNotUnderstand')
                )
                return None
            return handler(self, hermes, intent_message)
        return wrapper

    @check_confidence_score
    @check_site_id
    def handler_relay_turn_on(self, hermes, intent_message):
        print("Relay Turn On")
        hermes.publish_end_session(
            intent_message.session_id,
            self.__i18n.get('relayTurnOn')
        )

    @check_confidence_score
    @check_site_id
    def handler_relay_turn_off(self, hermes, intent_message):
        print("Relay Turn Off")
        hermes.publish_end_session(
            intent_message.session_id,
            self.__i18n.get('relayTurnOff')
        )

    def start_block(self):
        print('START BLOCK')
        with Hermes(self.__mqtt_addr) as h:
            h.subscribe_intent(
                'lightTurnOn',
                self.handler_relay_turn_on
            ) \
             .subscribe_intent(
                'lightTurnOff',
                self.handler_relay_turn_off
            ) \
             .start()