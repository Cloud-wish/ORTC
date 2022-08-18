import copy

class Trie:
    def __init__(self, l: int, r: int, w: set) -> None:
        self.l = l
        self.r = r
        self.w = w
        pass

tree = []

tree_siz = 0

def get_binary(ip: str, mask_length: int) -> list:
    ip=ip.split(".")
    # print(ip)
    res = []
    for i in range(4):
        ip[i] = int(ip[i])
        for j in range(8):
            if(i*8 + j + 1 > mask_length):
                break
            if((ip[i] & (1 << (7 - j))) != 0):
                res.append(1)
            else:
                res.append(0)
    return res

def add(l: int, r: int, w: set) -> int:
    global tree_siz
    tree.append(Trie(l, r, w))
    tree_siz += 1
    return tree_siz - 1

def insert(ip_bin: list, nxt) -> None:
    cur = 0
    for i in range(len(ip_bin)):
        if(ip_bin[i] == 0):
            # left
            if(tree[cur].l == -1):
                # add new node
                tree[cur].l = add(-1, -1, set())
            cur = tree[cur].l
        else:
            # right
            if(tree[cur].r == -1):
                # add new node
                tree[cur].r = add(-1, -1, set())
            cur = tree[cur].r
        # print(ip_bin[i], cur, tree[cur].w)
    tree[cur].w = set([nxt])

def dfs_add_son(p: int) -> None:
    if(tree[p].l == -1 and tree[p].r == -1):
        return
    elif(tree[p].l == -1):
        tree[p].l = add(-1, -1, set())
    elif(tree[p].r == -1):
        tree[p].r = add(-1, -1, set())
    dfs_add_son(tree[p].l)
    dfs_add_son(tree[p].r)

def dfs_pushdown_w(p: int, fa_w: set) -> None:
    if(tree[p].l == -1 and tree[p].r == -1):
        if(len(tree[p].w) == 0):
            tree[p].w = copy.deepcopy(fa_w)
        return
    if(len(tree[p].w) > 0):
        fa_w = copy.deepcopy(tree[p].w)
        tree[p].w = set()
    dfs_pushdown_w(tree[p].l, fa_w)
    dfs_pushdown_w(tree[p].r, fa_w)

def do_calc_set(a_set: set, b_set: set) -> list:
    a_intersect_b = a_set.intersection(b_set)
    if(len(a_intersect_b) > 0):
        return a_intersect_b
    else:
        return a_set.union(b_set)

def dfs_calc_set(p: int) -> None:
    if(tree[p].l == -1 and tree[p].r == -1):
        return
    dfs_calc_set(tree[p].l)
    dfs_calc_set(tree[p].r)
    tree[p].w = do_calc_set(tree[tree[p].l].w, tree[tree[p].r].w)

pre_node = [0]

def get_intersect(a: set, b: set) -> list:
    return a.intersection(b)

def dfs_remove_repeat(p: int) -> None:
    for i in range(len(pre_node) - 1 , -1, -1):
        if(len(tree[pre_node[i]].w) > 0):
            fa_w = tree[pre_node[i]].w
            break
    intersect = get_intersect(tree[p].w, fa_w)
    # print(tree[p].w, fa_w)
    if(len(intersect) > 0):
        tree[p].w.clear()
    else:
        while(len(tree[p].w) > 1):
            tree[p].w.pop()
    if(tree[p].l == -1 and tree[p].r == -1):
        return
    pre_node.append(p)
    dfs_remove_repeat(tree[p].l)
    dfs_remove_repeat(tree[p].r)
    pre_node.pop()

pre_binary = []

def binary_to_ip() -> str:
    # return "".join(pre_binary)
    binary = copy.deepcopy(pre_binary)
    while(len(binary) < 32):
        binary.append("0")
    # print(binary)
    return f"{int(''.join(binary[0:8]), base=2)}.{int(''.join(binary[8:16]), base=2)}.{int(''.join(binary[16:24]), base=2)}.{int(''.join(binary[24:32]), base=2)}"

def output(w: set, p: int) -> None:
    print(f"IP: {binary_to_ip()} mask length:{len(pre_binary)} nxt: {w} p:{p}")

def dfs_get_result(p: int) -> None:
    # print(p, "".join(pre_binary))
    if(len(tree[p].w) > 0):
        output(tree[p].w, p)
    if(tree[p].l == -1 and tree[p].r == -1):
        return
    if(tree[p].l != -1):
        pre_binary.append("0")
        dfs_get_result(tree[p].l)
        pre_binary.pop()
    if(tree[p].r != -1):
        pre_binary.append("1")
        dfs_get_result(tree[p].r)
        pre_binary.pop()

with open("data.txt", "r", encoding="UTF-8") as f:
    raw_data = f.read().split(";")
    for route in raw_data:
        if(len(route) == 0):
            break
        route = route.split(" ")
        if(len(route) == 1):
            if(route[0] == "empty"):
                add(-1, -1, set())
            else:
                add(-1, -1, set([route[0]]))
            continue
        route[0] = route[0].lstrip()
        # print(route)
        # 0:IP 1:mask length 2:nxt
        ip_bin = get_binary(route[0], int(route[1]))
        # print(ip_bin)
        insert(ip_bin, route[2])
        # dfs_get_result(0)

print("Initial")
dfs_get_result(0)

# Pass 1
dfs_add_son(0)

dfs_pushdown_w(0, set())

# print("After Pass 1")
# dfs_get_result(0)

# Pass 2
dfs_calc_set(0)

# print("After Pass 2")
# dfs_get_result(0)

# Pass 3
dfs_remove_repeat(tree[0].l)
dfs_remove_repeat(tree[0].r)

# Output Result
print("Result:")
dfs_get_result(0)