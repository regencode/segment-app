import numpy as np
import torch
from torch import nn
from torchvision.models import resnet50
from torch.nn import functional as F

# DeepLab V3+ Model

class ASPP(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(ASPP, self).__init__()
        self.atrous_block1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0, dilation=1, bias=False)
        self.atrous_block2 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=6, dilation=6, bias=False)
        self.atrous_block3 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=12, dilation=12, bias=False)
        self.atrous_block4 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=18, dilation=18, bias=False)
        self.global_avg_pool = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, bias=False)
        )
        
        self.conv1 = nn.Conv2d(out_channels * 5, out_channels, kernel_size=1, stride=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, x):
        size = x.shape[-2:]
        block1 = self.atrous_block1(x)
        block2 = self.atrous_block2(x)
        block3 = self.atrous_block3(x)
        block4 = self.atrous_block4(x)
        global_pool = self.global_avg_pool(x)
        global_pool = F.interpolate(global_pool, size=size, mode='bilinear', align_corners=False)

        x = torch.cat([block1, block2, block3, block4, global_pool], dim=1)
        x = self.conv1(x)
        x = self.bn1(x)
        return self.relu(x)

class DeepLabV3Plus(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DeepLabV3Plus, self).__init__()

        # Backbone: ResNet-50
        self.backbone = resnet50(pretrained=True)
        if in_channels != 3:
            self.backbone.conv1 = nn.Conv2d(in_channels, 64, kernel_size=7, stride=2, padding=3, bias=False)

        self.low_level_channels = 256
        self.aspp = ASPP(2048, 256)

        # Decoder
        self.decoder_conv1 = nn.Conv2d(self.low_level_channels, 48, kernel_size=1, bias=False)
        self.decoder_bn1 = nn.BatchNorm2d(48)
        self.decoder_relu = nn.ReLU()
        
        self.decoder_conv2 = nn.Conv2d(304, 256, kernel_size=3, padding=1, bias=False)
        self.decoder_bn2 = nn.BatchNorm2d(256)
        self.decoder_conv3 = nn.Conv2d(256, 256, kernel_size=3, padding=1, bias=False)
        self.decoder_bn3 = nn.BatchNorm2d(256)
        self.classifier = nn.Conv2d(256, out_channels, kernel_size=1)

    def forward(self, x):
        size = x.shape[-2:]

        # Encoder
        x = self.backbone.conv1(x)
        x = self.backbone.bn1(x)
        x = self.backbone.relu(x)
        x = self.backbone.maxpool(x)

        low_level_features = self.backbone.layer1(x)
        x = self.backbone.layer2(low_level_features)
        x = self.backbone.layer3(x)
        x = self.backbone.layer4(x)

        x = self.aspp(x)
        x = F.interpolate(x, size=low_level_features.shape[-2:], mode='bilinear', align_corners=False)

        # Decoder
        low_level_features = self.decoder_conv1(low_level_features)
        low_level_features = self.decoder_bn1(low_level_features)
        low_level_features = self.decoder_relu(low_level_features)

        x = torch.cat([x, low_level_features], dim=1)
        x = self.decoder_conv2(x)
        x = self.decoder_bn2(x)
        x = self.decoder_relu(x)
        x = self.decoder_conv3(x)
        x = self.decoder_bn3(x)
        x = self.decoder_relu(x)

        x = self.classifier(x)
        x = F.interpolate(x, size=size, mode='bilinear', align_corners=False)
        return x

class DeepLabRunner:
    def __init__(self, device):
        self.device = torch.device(device)
        self.model = DeepLabV3Plus(3, 2)
        self.model.load_state_dict(torch.load("utils/dv3p_best_checkpoint.pth", weights_only=True, map_location=self.device))

    def forward(self, input_array : np.array): # input shape (W, H, C)
        self.model.eval()
        # convert data to torch float tensor
        x = input_array[np.newaxis, :, :, :] # (1, W, H, C)
        x = torch.from_numpy(x).to(torch.float32)
        x = (x - x.min()) / (x.max() - x.min()) # normalize
        x = torch.permute(x, (0, 3, 1, 2)) # (1, C, W, H)

        output = self.model(x) # (1, 2, W, H)

        output = torch.squeeze(output) # (2, W, H)
        output = torch.argmax(output, dim=0) # (W, H)
        output = output * 255
        output = torch.clamp(output, 0, 255).to(torch.uint8)
        output = output.detach().numpy() # (W, H)

        print(output.shape)
        print(output)
        return output