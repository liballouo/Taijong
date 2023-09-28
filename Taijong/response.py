import torch
import torch.nn as nn

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# model
class Discard_Model(nn.Module):
    def __init__(self):
        super(Discard_Model, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=256, kernel_size=3, stride=1, padding='same')
        self.conv2 = nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding='same')
        self.conv_last = nn.Conv1d(in_channels=256, out_channels=32, kernel_size=3, stride=1)
        # self.fc = nn.Linear(32*34, 1024)
        self.fc1 = nn.Linear(1024, 256)
        self.fc2 = nn.Linear(256, 34)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        batch_size = x.size(0)
        out = self.conv1(x)
        out = self.relu(out)
        for i in range(2):
          out = self.conv2(out)
          out = self.relu(out)

        out = self.conv_last(out)
        out = self.relu(out)
        out = out.view(batch_size, -1)  # Flatten the output of convolutional layer
        # out = self.fc(out)
        out = self.fc1(out)
        out = self.fc2(out)
        out = self.softmax(out)
        return out

class Pong_Model(nn.Module):
    def __init__(self):
        super(Pong_Model, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=2, out_channels=256, kernel_size=3, stride=1, padding='same')
        self.conv2 = nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding='same')
        self.conv_last = nn.Conv1d(in_channels=256, out_channels=32, kernel_size=3, stride=1)
        # self.fc = nn.Linear(32*34, 1024)
        self.fc1 = nn.Linear(1024, 256)
        self.fc2 = nn.Linear(256, 2)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        batch_size = x.size(0)
        out = self.conv1(x)
        out = self.relu(out)
        for i in range(2):
          out = self.conv2(out)
          out = self.relu(out)

        out = self.conv_last(out)
        out = self.relu(out)
        out = out.view(batch_size, -1)  # Flatten the output of convolutional layer
        # out = self.fc(out)
        out = self.fc1(out)
        out = self.fc2(out)
        out = self.softmax(out)
        return out

class Kong_Model(nn.Module):
    def __init__(self):
        super(Kong_Model, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=2, out_channels=256, kernel_size=3, stride=1, padding='same')
        self.conv2 = nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding='same')
        self.conv_last = nn.Conv1d(in_channels=256, out_channels=32, kernel_size=3, stride=1)
        # self.fc = nn.Linear(32*34, 1024)
        self.fc1 = nn.Linear(1024, 256)
        self.fc2 = nn.Linear(256, 2)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        batch_size = x.size(0)
        out = self.conv1(x)
        out = self.relu(out)
        for i in range(2):
          out = self.conv2(out)
          out = self.relu(out)

        out = self.conv_last(out)
        out = self.relu(out)
        out = out.view(batch_size, -1)  # Flatten the output of convolutional layer
        # out = self.fc(out)
        out = self.fc1(out)
        out = self.fc2(out)
        out = self.softmax(out)
        return out

class Chow_Model(nn.Module):
    def __init__(self):
        super(Chow_Model, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=2, out_channels=256, kernel_size=3, stride=1, padding='same')
        self.conv2 = nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding='same')
        self.conv_last = nn.Conv1d(in_channels=256, out_channels=32, kernel_size=3, stride=1)
        self.fc1 = nn.Linear(1024, 256)
        self.fc2 = nn.Linear(256, 4)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        batch_size = x.size(0)
        out = self.conv1(x)
        out = self.relu(out)
        for i in range(2):
          out = self.conv2(out)
          out = self.relu(out)

        out = self.conv_last(out)
        out = self.relu(out)
        out = out.view(batch_size, -1)  # Flatten the output of convolutional layer
        # out = self.fc(out)
        out = self.fc1(out)
        out = self.fc2(out)
        out = self.softmax(out)
        return out

def discard_tile(hand_tiles):
    # for testing 
    hand_tiles = [int(num) for num in hand_tiles]

    # Convert hand tiles to (1, 1, 34) tensor
    hand_tiles = torch.tensor(hand_tiles, dtype=torch.float32)
    hand_tiles = hand_tiles.reshape(-1, 1, 34)

    # Load model
    discard_model = torch.load("./Discard_model/best_model.pth", map_location='cpu')
    # Model initiation 
    model = Discard_Model()
    criterion = nn.CrossEntropyLoss()
    learning_rate = 0.0001
    # Copy the information of trainded model to the model    
    model.load_state_dict(discard_model['model_state_dict'])
    model = model.to(device)
    criterion = criterion.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    optimizer.load_state_dict(discard_model['optimizer_state_dict'])

    model.eval()

    output = model(hand_tiles)
    output = torch.max(output, 1)

    return output

def Chow(throw, hand_tiles):
    # input data for the model
    input_data = [throw, hand_tiles]

    # Convert hand tiles to (1, 2, 34) tensor
    input_data = torch.tensor(input_data, dtype=torch.float32)
    input_data = input_data.reshape(-1, 2, 34)

    # Load model
    discard_model = torch.load("./Chow_model/best_model.pth", map_location='cpu')
    # Model initiation 
    model = Chow_Model()
    criterion = nn.CrossEntropyLoss()
    learning_rate = 0.0001
    # Copy the information of trainded model to the model    
    model.load_state_dict(discard_model['model_state_dict'])
    model = model.to(device)
    criterion = criterion.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    optimizer.load_state_dict(discard_model['optimizer_state_dict'])

    model.eval()

    output = model(input_data)
    # output = torch.max(output, 1)

    return output

def Pong(throw, hand_tiles):
    # input data for the model
    input_data = [throw, hand_tiles]

    # Convert hand tiles to (1, 2, 34) tensor
    input_data = torch.tensor(input_data, dtype=torch.float32)
    input_data = input_data.reshape(-1, 2, 34)

    # Load model
    discard_model = torch.load("./Pong_model/best_model.pth", map_location='cpu')
    # Model initiation 
    model = Pong_Model()
    criterion = nn.CrossEntropyLoss()
    learning_rate = 0.0001
    # Copy the information of trainded model to the model    
    model.load_state_dict(discard_model['model_state_dict'])
    model = model.to(device)
    criterion = criterion.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    optimizer.load_state_dict(discard_model['optimizer_state_dict'])

    model.eval()

    output = model(input_data)
    # output = torch.max(output, 1)

    return output

def Kong(throw, hand_tiles):
    # input data for the model
    input_data = [throw, hand_tiles]

    # Convert hand tiles to (1, 2, 34) tensor
    input_data = torch.tensor(input_data, dtype=torch.float32)
    input_data = input_data.reshape(-1, 2, 34)

    # Load model
    discard_model = torch.load("./Kong_model/best_model.pth", map_location='cpu')
    # Model initiation 
    model = Kong_Model()
    criterion = nn.CrossEntropyLoss()
    learning_rate = 0.0001
    # Copy the information of trainded model to the model    
    model.load_state_dict(discard_model['model_state_dict'])
    model = model.to(device)
    criterion = criterion.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    optimizer.load_state_dict(discard_model['optimizer_state_dict'])

    model.eval()

    output = model(input_data)
    # output = torch.max(output, 1)

    return output


# Testing
# Discard
# test = discard_tile([1, 2, 0, 0, 1, 0, 0, 1, 2, 1, 1, 2, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
# print(test)

# Chow
# test = Chow([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0, 2, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0])
# print(test[0][1])

# Pong
# test = Pong([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0])
# a = test[0][1]
# print(a)

# Kong
# test = Kong([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 2, 0, 3, 0, 0, 1, 0])
# print(test)