import torch
import torch.nn as nn
import torch.nn.functional as F
from libbaghchal import Baghchal, TransitionHistoryInstance

LEARNING_RATE = 0.001


class BaghchalActorCritic(nn.Module):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    gamma = 0.0

    optimizer: torch.optim.Adam

    def __init__(self):
        super(BaghchalActorCritic, self).__init__()

        # Convolutional layers
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=2),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, padding=2),
            nn.ReLU(),
        )

        # Tiger Actor-specific Layers
        self.tiger_actor_fc = nn.Sequential(
            nn.Linear((9 * 9 * 128 + 6), 512),
            nn.ReLU(),
            nn.Linear(512, 192),  # 192 possible actions for tiger movement
            nn.Softmax(),
        )

        # Goat Movement Actor-specific Layers
        self.goat_actor_fc = nn.Sequential(
            nn.Linear((9 * 9 * 128 + 6), 512),
            nn.ReLU(),
            nn.Linear(512, 112),  # 112 possible actions for goat movement
            nn.Softmax(),
        )

        # Goat Placement Actor-specific Layers
        self.goat_placement_actor_fc = nn.Sequential(
            nn.Linear((9 * 9 * 128 + 6), 512),
            nn.ReLU(),
            nn.Linear(512, 25),  # 25 possible actions for goat placement
            nn.Softmax(),
        )

        # V-specific Layer
        self.v_fc = nn.Sequential(nn.Linear((9 * 9 * 128 + 6), 512), nn.Linear(512, 1))

        self.optimizer = torch.optim.Adam(self.parameters(), lr=LEARNING_RATE)

    def forward_v(self, input):
        board_tiger = input[:25].view(-1)
        board_goat = input[25:50].view(-1)
        board_blank = input[50:75].view(-1)

        others = input[125:131].view(-1)

        x_critic = torch.cat(
            (board_tiger, board_goat, board_blank),
            dim=-1,
        )
        x_critic = x_critic.view(-1, 3, 5, 5)

        critic_conv_out = self.conv_layers(x_critic)
        critic_conv_out = critic_conv_out.view((-1,))

        merged = torch.cat((critic_conv_out, others), dim=-1)

        # Forward pass for critic network
        critic_output = self.v_fc(merged)

        return critic_output

    def forward_actor(self, input):
        if not torch.is_tensor(input):
            input = torch.tensor(input, dtype=torch.float32).to(self.device)
        board_tiger = input[:25].view(-1)
        board_goat = input[25:50].view(-1)
        board_blank = input[50:75].view(-1)

        others = input[125:131].view(-1)

        x = torch.cat((board_tiger, board_goat, board_blank), dim=-1)
        x = x.view(-1, 5, 5)

        conv_out = self.conv_layers(x)
        conv_out = conv_out.view((-1,))

        merged = torch.cat((conv_out, others), dim=-1)

        if input[125] == 1:
            actor_output = self.goat_actor_fc(merged)
        elif input[130] == 1:
            actor_output = self.tiger_actor_fc(merged)
        else:
            actor_output = self.goat_placement_actor_fc(merged)

        return actor_output

    def train_step(self, transition: TransitionHistoryInstance):
        states = transition.state[0][0]
        states = torch.tensor(states, dtype=torch.float32).to(self.device)

        actions = torch.tensor(transition.move_vector(), dtype=torch.long).to(
            self.device
        )
        rewards = torch.tensor(transition.move_reward, dtype=torch.float32).to(
            self.device
        )

        if transition.is_terminal:
            next_states = states
        else:
            next_states = transition.resulting_state[0][0]
            next_states = torch.tensor(next_states, dtype=torch.float32).to(self.device)

        # Compute critic predictions for current and next states
        v_value = self.forward_v(states)
        next_v_value = self.forward_v(next_states)

        # Compute TD targets for the critic
        td_targets = rewards + self.gamma * next_v_value * (
            1 - int(transition.is_terminal)
        )

        # Compute advantages as the TD errors
        advantages = td_targets - v_value

        # Compute actor's log probabilities of selected actions
        action_probs = self.forward_actor(states)

        # Perform optimization step
        self.optimizer.zero_grad()

        action_dist = torch.distributions.Categorical(action_probs)
        log_probs = action_dist.log_prob(actions)
        # action_log_probs = log_probs.gather(-1, actions).squeeze(-1)

        # Compute actor and critic losses
        actor_loss = -log_probs * advantages.detach()

        # critic_loss = F.smooth_l1_loss(v_value, td_targets.detach())
        critic_loss = advantages.pow(2)

        # Compute total loss
        total_loss = actor_loss + critic_loss

        # nn.utils.clip_grad_norm_(self.parameters(), 1.0)
        self.optimizer.step()

        return total_loss.mean().item()
