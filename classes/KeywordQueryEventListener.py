from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.search.SortedList import get_score

import logging

logger = logging.getLogger(__name__)

class KeywordQueryEventListener(EventListener):
    def sort_based_on_similarity(self, options, argument):
        score = []
        for option in options:
            score.append(get_score(argument, option))

        zip_score_option = list(zip(score, options))
        sorted_zip = sorted(zip_score_option, key=lambda x: x[0], reverse=True)
        score, sorted_options = zip(*sorted_zip)
        return sorted_options  
        

    def on_event(self, event, extension):
        
        options = ["connect", "reconnect", "disconnect"]
                
        argument = event.get_argument()
        if argument:
            options = self.sort_based_on_similarity(options, argument)
                
        items = []
        for option in options:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=option,
                on_enter=ExtensionCustomAction(
                    {"command": option}, keep_app_open=True))
            )        

        return RenderResultListAction(items)