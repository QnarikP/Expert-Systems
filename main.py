import pygame
from graphviz import Digraph


# ------------------ Helper Functions ------------------

def draw_text_lines(surface, lines, start_pos, font, color, line_spacing=8):
    """Draw a list of text lines starting at start_pos with given line spacing."""
    x, y = start_pos
    for line in lines:
        rendered = font.render(line, True, color)
        surface.blit(rendered, (x, y))
        y += rendered.get_height() + line_spacing


# ------------------ Core Expert System Classes ------------------

class KnowledgeBase:
    def __init__(self):
        # Facts are stored as a set and rules as a list.
        self.facts = set()
        self.rules = []

    def add_fact(self, fact):
        self.facts.add(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def reset_facts(self):
        self.facts = set()


class Rule:
    def __init__(self, conditions, conclusion):
        """
        conditions: list of facts required for the rule to fire
        conclusion: the fact to add if conditions are met
        """
        self.conditions = conditions
        self.conclusion = conclusion

    def is_applicable(self, facts):
        # Check if all conditions exist in the current set of facts.
        return all(condition in facts for condition in self.conditions)


class InferenceEngine:
    def __init__(self, kb, log_callback=None):
        self.kb = kb
        self.log_callback = log_callback

    def forward_chain(self):
        new_fact_added = True
        while new_fact_added:
            new_fact_added = False
            for rule in self.kb.rules:
                if rule.is_applicable(self.kb.facts) and rule.conclusion not in self.kb.facts:
                    message = f"Rule fired: IF {rule.conditions} THEN {rule.conclusion}"
                    print(message)
                    if self.log_callback:
                        self.log_callback(message)
                    self.kb.add_fact(rule.conclusion)
                    new_fact_added = True


class Visualizer:
    def __init__(self, kb):
        self.kb = kb

    def visualize(self, filename='expert_system_visualization'):
        dot = Digraph(comment="Expert System Knowledge Base")
        # Create nodes for facts (blue ellipses)
        for fact in self.kb.facts:
            dot.node(fact, fact, shape='ellipse', style='filled', fillcolor='lightblue')
        # Create nodes for rules (grey boxes) with edges
        for i, rule in enumerate(self.kb.rules):
            rule_node = f"Rule_{i + 1}"
            rule_label = "IF\n" + "\nAND\n".join(rule.conditions) + f"\nTHEN\n{rule.conclusion}"
            dot.node(rule_node, rule_label, shape='box', style='filled', fillcolor='lightgrey')
            for cond in rule.conditions:
                dot.edge(cond, rule_node)
            dot.edge(rule_node, rule.conclusion)
        dot.render(filename, view=True, format='png')
        return dot


# ------------------ Advanced User Interface with Pygame ------------------

class UserInterface:
    def __init__(self, kb):
        pygame.init()
        self.kb = kb
        self.screen_width = 800
        self.screen_height = 650
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Professional Expert System - Medical Diagnosis")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 20)
        self.large_font = pygame.font.SysFont("arial", 24, bold=True)

        # Define layout coordinates.
        self.input_box = pygame.Rect(50, 50, 500, 32)
        self.add_button = pygame.Rect(570, 50, 100, 32)
        self.submit_button = pygame.Rect(570, 90, 100, 32)
        self.reset_button = pygame.Rect(570, 130, 100, 32)
        self.visualize_button = pygame.Rect(570, 170, 100, 32)

        # Radio buttons for domain selection.
        self.radio_buttons = []
        radio_start_x = 50
        radio_start_y = 100
        self.domain_options = ["Respiratory", "Cardiac", "Both"]
        self.selected_domain = "Both"
        for option in self.domain_options:
            rect = pygame.Rect(radio_start_x, radio_start_y, 20, 20)
            self.radio_buttons.append((rect, option))
            radio_start_x += 120

        # Panels for data display.
        self.entered_panel = pygame.Rect(50, 150, 300, 120)  # Entered Facts.
        self.results_panel = pygame.Rect(50, 280, 300, 120)  # Inference Output.
        self.log_panel = pygame.Rect(400, 200, 350, 120)  # Event Log.
        self.visual_panel = pygame.Rect(50, 420, 700, 200)  # Visualization Panel.

        self.input_text = ""
        self.entered_facts = []  # Stores facts entered one by one.
        self.inferred_facts = []  # Results after inference.
        self.event_log = []  # Log of fired rules.
        self.visual_image = None  # Holds loaded visualization image.
        self.visualized = False

        self.update_rules()

    def update_rules(self):
        self.kb.rules = []
        # Respiratory rules (if selected or Both).
        if self.selected_domain in ["Respiratory", "Both"]:
            r1 = Rule(["fever", "cough"], "possible_flu")
            r2 = Rule(["body_aches", "possible_flu"], "diagnose_flu")
            r3 = Rule(["fever", "loss_of_taste"], "possible_covid")
            r4 = Rule(["cough", "loss_of_taste"], "possible_covid")
            r5 = Rule(["sore_throat", "runny_nose"], "possible_cold")
            r6 = Rule(["possible_covid", "loss_of_taste"], "diagnose_covid")
            r7 = Rule(["possible_cold", "mild_fever"], "diagnose_cold")
            self.kb.add_rule(r1)
            self.kb.add_rule(r2)
            self.kb.add_rule(r3)
            self.kb.add_rule(r4)
            self.kb.add_rule(r5)
            self.kb.add_rule(r6)
            self.kb.add_rule(r7)
        # Cardiac rules (if selected or Both).
        if self.selected_domain in ["Cardiac", "Both"]:
            r8 = Rule(["chest_pain", "shortness_of_breath", "diaphoresis"], "possible_heart_attack")
            r9 = Rule(["possible_heart_attack", "nausea"], "diagnose_heart_attack")
            self.kb.add_rule(r8)
            self.kb.add_rule(r9)

    def log_event(self, message):
        self.event_log.append(message)
        if len(self.event_log) > 10:
            self.event_log.pop(0)

    def process_add_fact(self):
        if self.input_text.strip() != "":
            fact = self.input_text.strip()
            self.entered_facts.append(fact)
            self.log_event(f"Added fact: {fact}")
            self.input_text = ""

    def process_submit(self):
        self.kb.reset_facts()
        self.event_log = []
        initial_facts = set(self.entered_facts)  # Store initial entered facts.
        self.inferred_facts = []
        for fact in self.entered_facts:
            self.kb.add_fact(fact)
        engine = InferenceEngine(self.kb, log_callback=self.log_event)
        engine.forward_chain()
        self.inferred_facts = list(self.kb.facts - initial_facts)  # Exclude inputs from inference output.

    def process_reset(self):
        self.input_text = ""
        self.entered_facts = []
        self.inferred_facts = []
        self.event_log = []
        self.kb.reset_facts()
        self.visual_image = None
        self.visualized = False

    def process_visualize(self):
        visualizer = Visualizer(self.kb)
        visualizer.visualize("expert_system_visualization")
        try:
            self.visual_image = pygame.image.load("expert_system_visualization.png")
            self.visual_image = pygame.transform.scale(self.visual_image,
                                                       (self.visual_panel.width, self.visual_panel.height))
            self.visualized = True
        except Exception as e:
            self.log_event(f"Visualization error: {e}")

    def draw_button(self, rect, text, color, text_color):
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        txt = self.font.render(text, True, text_color)
        txt_rect = txt.get_rect(center=rect.center)
        self.screen.blit(txt, txt_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle text input.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.process_add_fact()
                    else:
                        self.input_text += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.add_button.collidepoint(mouse_pos):
                        self.process_add_fact()
                    if self.submit_button.collidepoint(mouse_pos):
                        self.process_submit()
                    if self.reset_button.collidepoint(mouse_pos):
                        self.process_reset()
                    if self.visualize_button.collidepoint(mouse_pos):
                        self.process_visualize()
                    # Domain selection via radio buttons.
                    for rect, label in self.radio_buttons:
                        if rect.collidepoint(mouse_pos):
                            self.selected_domain = label
                            self.update_rules()

            self.draw()
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()

    def draw(self):
        self.screen.fill((245, 245, 245))  # Light grey background.

        # Draw Title.
        title = self.large_font.render("Professional Expert System - Medical Diagnosis", True, (30, 30, 30))
        self.screen.blit(title, (50, 10))

        # Draw input box and its label.
        input_label = self.font.render("Enter a symptom (fact):", True, (0, 0, 0))
        self.screen.blit(input_label, (50, 30))
        pygame.draw.rect(self.screen, (200, 200, 200), self.input_box, 2, border_radius=8)
        input_surface = self.font.render(self.input_text, True, (0, 0, 0))
        self.screen.blit(input_surface, (self.input_box.x + 5, self.input_box.y + 5))

        # Draw professional buttons.
        self.draw_button(self.add_button, "Add Fact", (70, 130, 180), (255, 255, 255))
        self.draw_button(self.submit_button, "Submit", (34, 139, 34), (255, 255, 255))
        self.draw_button(self.reset_button, "Reset", (178, 34, 34), (255, 255, 255))
        self.draw_button(self.visualize_button, "Visualize", (72, 61, 139), (255, 255, 255))

        # Domain selection radio buttons.
        domain_label = self.font.render("Select Domain:", True, (0, 0, 0))
        self.screen.blit(domain_label, (50, 80))
        for rect, label in self.radio_buttons:
            pygame.draw.ellipse(self.screen, (0, 0, 0), rect, 2)
            if label == self.selected_domain:
                pygame.draw.ellipse(self.screen, (0, 150, 0), rect)
            radio_text = self.font.render(label, True, (0, 0, 0))
            self.screen.blit(radio_text, (rect.right + 5, rect.y))

        # Draw Entered Facts Panel.
        pygame.draw.rect(self.screen, (220, 250, 250), self.entered_panel, border_radius=12)
        entered_header = self.font.render("Entered Facts:", True, (0, 0, 150))
        self.screen.blit(entered_header, (self.entered_panel.x + 5, self.entered_panel.y + 5))
        draw_text_lines(self.screen, [f"- {fact}" for fact in self.entered_facts],
                        (self.entered_panel.x + 5, self.entered_panel.y + 30),
                        self.font, (0, 0, 0), line_spacing=8)

        # Draw Inference Output Panel.
        pygame.draw.rect(self.screen, (220, 250, 220), self.results_panel, border_radius=12)
        results_header = self.font.render("Inference Output:", True, (0, 100, 0))
        self.screen.blit(results_header, (self.results_panel.x + 5, self.results_panel.y + 5))
        draw_text_lines(self.screen, [f"- {fact}" for fact in self.inferred_facts],
                        (self.results_panel.x + 5, self.results_panel.y + 30),
                        self.font, (0, 100, 0), line_spacing=8)

        # Draw Event Log Panel.
        pygame.draw.rect(self.screen, (250, 250, 220), self.log_panel, border_radius=12)
        log_header = self.font.render("Event Log:", True, (150, 0, 0))
        self.screen.blit(log_header, (self.log_panel.x + 5, self.log_panel.y + 5))
        draw_text_lines(self.screen, self.event_log,
                        (self.log_panel.x + 5, self.log_panel.y + 35),
                        self.font, (0, 0, 0), line_spacing=8)

        # Draw Visualization Panel.
        pygame.draw.rect(self.screen, (230, 230, 230), self.visual_panel, 2, border_radius=12)
        vis_header = self.font.render("Knowledge Base Visualization:", True, (0, 0, 0))
        self.screen.blit(vis_header, (self.visual_panel.x + 5, self.visual_panel.y - 25))
        if self.visualized and self.visual_image:
            self.screen.blit(self.visual_image, (self.visual_panel.x, self.visual_panel.y))
        else:
            placeholder = self.font.render("Click 'Visualize' to view KB", True, (100, 100, 100))
            ph_rect = placeholder.get_rect(center=self.visual_panel.center)
            self.screen.blit(placeholder, ph_rect)


if __name__ == "__main__":
    kb = KnowledgeBase()
    ui = UserInterface(kb)
    ui.run()
