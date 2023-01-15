import pprint

warehouses = {
    "OH": {
        "sources": [('OR', 3)],
        "inventory": {
            "Acoustic Bloc Screen": 10,
            "Standing Desk": 100,
            "Office Chair": 12,
            "Drawer Organizer": 1,
            "Fire-proof Safe": 5
        }
    },
    "OR": {
        "sources": [('GA', 4)],
        "inventory": {
            "Acoustic Bloc Screen": 15,
            "Standing Desk": 2,
            "Drawer Organizer": 35,
            "Fire-proof Safe": 2
        },
    },
    "GA": {
        "sources": [('OR', 4), ('IA', 2), ('NH', 1)],
        "inventory": {
            "Acoustic Bloc Screen": 2,
            "Standing Desk": 2,
            "Office Chair": 2,
            "Drawer Organizer": 1,
        }
    },
    # (a, b)
    # [(a, b), (c, d)]
    # dict([(a, b), (c, d)])
    # let d = {'a': b, 'c': d}
    # d.a or d['a']
    "NH": {
        "sources": [('GA', 1), ('IA', 3)],
        "inventory": {
            "Acoustic Bloc Screen": 10,
            "Standing Desk": 2,
            "Office Chair": 2,
            "Drawer Organizer": 1,
        }
    },
    "IA": {
        "sources": [('OH', 1)],
        "inventory": {
            "Acoustic Bloc Screen": 10,
            "Standing Desk": 2,
            "Office Chair": 2,
            "Drawer Organizer": 1,
        }
    }
}

example_order = {
    'originating_wh': 'OH',
    'product': 'Acoustic Bloc Screen',
    'demand': 35
}


def find_moves(warehouses, order):
    demand = order['demand']
    product = order['product']
    total_time = 0
    moves = []
    visited_wh = []

    # returns quantity moved from current_wh
    def helper(current_wh, dest_wh=None):
        # nonlocal allows us to mutate the following vars
        nonlocal demand, moves, visited_wh, total_time

        # does the current wh carry our product?
        visited_wh.append(current_wh)
        wh_inventory = warehouses[current_wh]['inventory'].get(product, 0)

        # if the warehouse carries our product we will take what we can
        # if the warehouse inventory is greater than the demand, we'll take the demand
        # if the warehouse inventory is less than the demand, we'll take the warehouse inventory
        quantity_taken = 0
        if wh_inventory > 0:
            quantity_taken = min(demand, wh_inventory)
            # update demand in the case we took some
            demand -= quantity_taken

        for tup in warehouses[current_wh]["sources"]:
            (src_wh, time) = tup

            # if we're done, stop searching
            if demand == 0:
                continue

            # don't check inventories more than once
            if src_wh in visited_wh:
                continue

            quantity_taken += helper(src_wh, dest_wh=current_wh)

        if dest_wh is not None and current_wh != dest_wh and quantity_taken > 0:
            times = dict(warehouses[dest_wh]['sources'])
            time = times[current_wh]
            moves.append({
                'source': current_wh,
                'destination': dest_wh,
                'quantity': quantity_taken,
                'time': time
            })
            total_time += time

        return quantity_taken
    # end of helper
    
    helper(order['originating_wh'], dest_wh=None)

    # last case where the demand cannot be met by the total inventory between all warehouses
    if demand > 0:
        print("Not enough inventory available")
        return None

    return {
        'originating_wh': order['originating_wh'],
        'product': order['product'],
        'demand': order['demand'],
        'moves': moves,
        'total_time': total_time
    }


pp = pprint.PrettyPrinter()
pp.pprint(find_moves(warehouses, example_order))
