import json
import copy
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

firstDraw = True
drawNum = 0
figs = set()

class Node:
    def __init__(self, val, parent=None, id_num=-1):
        self.left = None
        self.right = None
        self.parent = parent
        self.val = val
        self.id_num = id_num

    def __repr__(self):
        return "id:" + str(self.id_num) + " val:" + str(self.val)


# Insert method to create nodes
class BST:
    def __init__(self):
        self.root = None
        self.node_id_to_val = {}
        self.posxs = {}
        self.posys = {}
        self.message_nodes = set()
        self.root_nodes = set()
        self.from_node_id = None
        self.to_node_id = None
        self.message_num = 0

    def insert(self, id_num, val):
        if id_num in self.node_id_to_val.keys():
            print("ID duplication assert")
            return
        if self.root is None:
            self.root = Node(val, None, id_num)
            self.node_id_to_val[id_num] = val
            return
        if self._insert(self.root, val, id_num):
            self.node_id_to_val[id_num] = val

    def _insert(self, node, val, id_num=-1):
        if val < node.val:
            if node.left is None:
                node.left = Node(val, node, id_num)
                return True
            else:
                return self._insert(node.left, val, id_num)
        elif val >= node.val:
            if node.right is None:
                node.right = Node(val, node, id_num)
                return True
            else:
                return self._insert(node.right, val, id_num)
        return False

    def findval(self, lkpval):
        return self._findval(self.root, lkpval)

    def _findval(self, node, lkpval):
        if lkpval < node.val:
            if node.left is None:
                return None
            return self._findval(node.left, lkpval)
        elif lkpval > node.val:
            if node.right is None:
                return None
            return self._findval(node.right, lkpval)
        else:
            return node

    def find_id(self, node_id):
        if node_id not in self.node_id_to_val.keys():
            print ("Search for non existing node id on the graph")
            assert False
        n = self._findval(self.root, self.node_id_to_val[node_id])
        while n is not None and n.id_num != node_id:
            n = self._findval(n.right, self.node_id_to_val[node_id])
        return n

    def get_lowest_common_ancestor(self, node_id_a, node_id_b):
        parent_set_a = self.collect_parents(node_id_a)
        n = self.find_id(node_id_b)
        while n is not None:
            if n in parent_set_a:
                return n
            n = n.parent
        assert False

    def collect_parents(self, node_id):
        parents = set()
        n = self.find_id(node_id)
        while n is not None:
            parents.add(n)
            n = n.parent
        return parents

# Print the tree
    def _print_tree(self, node):
        if node is None:
            return
        self._print_tree(node.left)
        print(str(node) + ","),
        self._print_tree(node.right)

    def print_tree(self):
        self._print_tree(self.root)
        print("\n")

    def _draw_tree(self, node, posx, posy, fig, ax, rad_times):
        if node is None:
            return
        rad = 1.5
        if node in self.message_nodes:
            ax.add_artist(plt.Circle((posx, posy), rad, color='red'))
        elif node in self.root_nodes:
            ax.add_artist(plt.Circle((posx, posy), rad, color='blue'))
        else:
            ax.add_artist(plt.Circle((posx, posy), rad, color='white'))
        ax.add_artist(plt.Circle((posx, posy), rad, color='black',linewidth=1, fill=None))
        #ax.text(posx, posy, str(node.id_num), fontsize=20, ha='center', va='center')
        ax.text(posx, posy, "id:" + str(node.id_num), fontsize=15, ha='center', va='bottom')
        ax.text(posx, posy, "val:" + str(node.val), fontsize=15, ha='center', va='top')
        self.posxs[node] = posx
        self.posys[node] = posy
        if node.parent is not None:
            ax.add_line(mlines.Line2D([posx, self.posxs[node.parent]], [posy, self.posys[node.parent]], zorder=0, color='black'))
        #elif node.parent is not None and node.parent.left == node:
        #    ax.add_line(mlines.Line2D([posx, posx - rad_times*rad], [posy, posy - rad_times*rad], zorder=0))
        #circle = plt.Circle((posx, posy), 0.4, color='black', linewidth=1, fill=None)
        self._draw_tree(node.left, posx - rad_times*rad, posy + 3*rad, fig, ax, max(2, rad_times/2))
        self._draw_tree(node.right, posx + rad_times*rad, posy + 3*rad, fig, ax, max(2, rad_times/2))

    def draw_tree(self):
        fig, ax = plt.subplots()
        if self.from_node_id is not None:
            ax.text(-40, 0, "Message #" + str(self.message_num), fontsize=20, ha='left', va='center')
            ax.text(-40, 2, "From: " + str(self.from_node_id), fontsize=20, ha='left', va='center')
        if self.to_node_id is not None:
            ax.text(-40, 4, "To: " + str(self.to_node_id), fontsize=20, ha='left', va='center')
        self._draw_tree(self.root, 0.0, 0.0, fig, ax, 16)
        ax.set_xlim(-50, 50)
        ax.set_ylim(50, -2)

        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('off')
        fig.axes[0].get_xaxis().set_visible(False)
        fig.axes[0].get_yaxis().set_visible(False)
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        global drawNum
        drawNum += 1
        if (drawNum % 5) == 3:
            for x in figs:
                plt.close(x)
            figs.clear()

        global firstDraw
        if firstDraw:
            plt.draw()
            plt.pause(0.1)  # <-------
            plt.waitforbuttonpress(0)
            firstDraw = False
            plt.close(fig)
        else:
        #plt.draw()
        #plt.pause(0.1)
            figs.add(fig)
            plt.show(block=False)
            raw_input("Press Enter to continue...")
        # raw_input("<Hit Enter To Close>")
        # plt.show()

    def send_message(self, from_node_id, to_node_id):
        new_root = self.get_lowest_common_ancestor(from_node_id, to_node_id)
        from_node = self.find_id(from_node_id)
        to_node = self.find_id(to_node_id)
        communication_cost = self.get_distance(from_node_id, to_node_id)
        self.root_nodes.clear()
        self.message_nodes.clear()
        self.message_nodes.add(from_node)
        self.message_nodes.add(to_node)

        self.message_num += 1
        self.from_node_id = from_node_id
        self.to_node_id = to_node_id

        if detail_level >= 2:
            self.draw_tree()

        self.root_nodes.clear()
        self.root_nodes.add(new_root)
        if detail_level >= 0.75:
            bst.draw_tree()

        if new_root != to_node:
            communication_cost += self.splay(from_node, new_root)
        elif to_node.val > from_node.val:
            communication_cost += self.splay(from_node, to_node.left)
        else:
            communication_cost += self.splay(from_node, to_node.right)

        if detail_level >= 1:
            self.draw_tree()

        if to_node.parent != from_node and from_node.parent != to_node:
            if to_node.val < from_node.val:
                communication_cost += self.splay(to_node, from_node.left)
            else:
                communication_cost += self.splay(to_node, from_node.right)
            if detail_level >= 1:
                self.draw_tree()

        if detail_level >= 0.75:
            bst.draw_tree()
        return communication_cost + 1

    def zig(self, node_a, node_b):
        if node_a == node_b.left:
            node_b.left = node_a.right
            if node_b.left is not None:
                node_b.left.parent = node_b
            node_a.right = node_b
        elif node_a == node_b.right:
            node_b.right = node_a.left
            if node_b.right is not None:
                node_b.right.parent = node_b
            node_a.left = node_b
        else:
            assert False
        if self.root == node_b:
            self.root = node_a
        elif node_b.parent.right == node_b:
            node_b.parent.right = node_a
        else:
            node_b.parent.left = node_a
        node_a.parent = node_b.parent
        node_b.parent = node_a
        if detail_level >= 2:
            self.draw_tree()

    def zigzig(self, node_a, node_b, node_c):
        if node_a == node_b.left and node_b == node_c.left:
            node_c.left = node_b.right
            if node_c.left is not None:
                node_c.left.parent = node_c
            node_b.right = node_c
            node_b.left = node_a.right
            if node_b.left is not None:
                node_b.left.parent = node_b
            node_a.right = node_b
        elif node_a == node_b.right and node_b == node_c.right:
            node_c.right = node_b.left
            if node_c.right is not None:
                node_c.right.parent = node_c
            node_b.left = node_c
            node_b.right = node_a.left
            if node_b.right is not None:
                node_b.right.parent = node_b
            node_a.left = node_b
        else:
            assert False
        if self.root == node_c:
            self.root = node_a
        elif node_c.parent.right == node_c:
            node_c.parent.right = node_a
        else:
            node_c.parent.left = node_a
        node_a.parent = node_c.parent
        node_b.parent = node_a
        node_c.parent = node_b
        if detail_level >= 2:
            self.draw_tree()

    def zigzag(self, node_a, node_b, node_c):
        if node_a == node_b.right and node_b == node_c.left:
            node_c.left = node_a.right
            if node_c.left is not None:
                node_c.left.parent = node_c
            node_b.right = node_a.left
            if node_b.right is not None:
                node_b.right.parent = node_b
            node_a.right = node_c
            node_a.left = node_b
        elif node_a == node_b.left and node_b == node_c.right:
            node_c.right = node_a.left
            if node_c.right is not None:
                node_c.right.parent = node_c
            node_b.left = node_a.right
            if node_b.left is not None:
                node_b.left.parent = node_b
            node_a.left = node_c
            node_a.right = node_b
        else:
            assert False
        if self.root == node_c:
            self.root = node_a
        elif node_c.parent.right == node_c:
            node_c.parent.right = node_a
        else:
            node_c.parent.left = node_a
        node_a.parent = node_c.parent
        node_b.parent = node_a
        node_c.parent = node_a
        if detail_level >= 2:
            self.draw_tree()

    def splay(self, node, root):
        root_par = root.parent
        step_num = 0
        while node.parent != root and node.parent != root_par:
            step_num += 1
            par = node.parent
            parpar = par.parent
            if (node == par.left and par == parpar.left) or (node == par.right and par == parpar.right):
                self.zigzig(node, par, parpar)
            else:
                self.zigzag(node, par, parpar)
        if node.parent == root:
            step_num += 1
            self.zig(node, root)
        # print "Splay step num: " + str(step_num)
        return step_num

    def get_distance(self, from_node_id, to_node_id):
        new_root = self.get_lowest_common_ancestor(from_node_id, to_node_id)
        from_node = self.find_id(from_node_id)
        to_node = self.find_id(to_node_id)
        n = from_node
        dist = 0
        while n != new_root:
            n = n.parent
            dist += 1
        n = to_node
        while n != new_root:
            n = n.parent
            dist += 1
        return dist


detail_level = 0.75
with open('minta.json') as data_file:
    data = json.load(data_file)

bst = BST()
non_adjusting_bst = BST()
nodes = data['Nodes']
messages = data['Messages']
for i in range(0, len(nodes)):
    bst.insert(i, nodes[i])
    non_adjusting_bst.insert(i, nodes[i])

if detail_level >= 0.5:
    bst.draw_tree()

adj_cost = 0
non_adj_cost = 0
for i in range(0, len(messages)):
    adj_cost += bst.send_message(messages[i][0], messages[i][1])
    non_adj_cost += non_adjusting_bst.get_distance(messages[i][0], messages[i][1])+1

if detail_level >= 0.5:
    bst.draw_tree()

print("Self adjusting network communication cost: " + str(adj_cost))
print("Static network communication cost: " + str(non_adj_cost))
    #bst.send_message(1, 3)
    #bst.send_message(4, 3)
    #bst.send_message(1, 3)



#bst = BST()
#bst.insert(0, 12)
#bst.insert(1, 13)
#bst.insert(2, 6)
#bst.insert(3, 14)
#bst.insert(4, 3)
#bst.insert(5, 2)
#bst.insert(6, 7)
#bst.insert(7, 8)
#bst.insert(8, 1)
#bst.insert(9, 9)
#bst.insert(10, 23)

#print(bst.findval(3))
#print(bst.findval(14))
#bst.print_tree()
#print(bst.find_id(0))
#bst.draw_tree()
n1 = bst.find_id(10)
n2 = bst.find_id(9)
n3 = bst.find_id(1)
#bst.zigzag(n1, n2, n3)
#bst.splay(bst.find_id(8), bst.root)
#bst.draw_tree()
#bst.splay(bst.find_id(10), bst.root)
#bst.draw_tree()

print("Finished")