from datetime import datetime
import pytz
def max_bid(item):
    return max(item.bids.all(),key=lambda x:x.bid_price)

def get_time():
    now=datetime.now()
    tz = pytz.timezone('Asia/Calcutta')
    time=now.astimezone(tz)
    return time 

def get_obj_with_bid(arr):
    items=[]
    for item in arr:
        bid_obj =  max_bid(item)
        cur_bid =  bid_obj.bid_price
        items.append([item,cur_bid])
    return items
def user_present_in_watch_list(item,user):
    present = False 
    if user.watch_list.filter(id=item.id).exists():
        present = True 
    return present
    