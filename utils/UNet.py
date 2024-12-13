import numpy as np
import torch
from torch import nn

class DoubleConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.blocks = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(out_channels),
        )
    def forward(self, x):
        x = self.blocks(x)
        return x

class Downsample(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv = DoubleConvBlock(in_channels, out_channels)
        self.maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
    
    def forward(self, x):
        x = self.conv(x)
        down = self.maxpool(x)
        return down, x

class Upconv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.upsample = nn.ConvTranspose2d(in_channels, out_channels, kernel_size=2, stride=2)
        self.conv = DoubleConvBlock(in_channels, out_channels)
    
    def forward(self, x, x_concat):
        x = self.upsample(x)
        x = torch.cat([x, x_concat], 1)
        x = self.conv(x) 
        return x



class UNet(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv1 = Downsample(in_channels, 64)
        self.conv2 = Downsample(64, 128)
        self.conv3 = Downsample(128, 256)
        self.conv4 = Downsample(256, 512)
        self.dropout = nn.Dropout(p=0.75)

        self.bottleneck = DoubleConvBlock(512, 1024)

        self.upconv1 = Upconv(1024, 512)
        self.upconv2 = Upconv(512, 256)
        self.upconv3 = Upconv(256, 128)
        self.upconv4 = Upconv(128, 64)
        self.out_conv = nn.Conv2d(64, out_channels, kernel_size=1)
    
    def forward(self, x):
        down_1, crop_1 = self.conv1(x)
        down_2, crop_2 = self.conv2(down_1)
        down_3, crop_3 = self.conv3(down_2)
        down_4, crop_4 = self.conv4(down_3)
        dropped = self.dropout(down_4)

        b = self.bottleneck(dropped)

        up_1 = self.upconv1(b, crop_4)
        up_2 = self.upconv2(up_1, crop_3)
        up_3 = self.upconv3(up_2, crop_2)
        up_4 = self.upconv4(up_3, crop_1)
        y = self.out_conv(up_4)
        return y

class UNetRunner:
    def __init__(self, device):
        self.device = torch.device(device)
        self.model = UNet(3, 2)
        self.model.load_state_dict(torch.load("utils/unet_best_checkpoint.pth", weights_only=True, map_location=self.device))

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