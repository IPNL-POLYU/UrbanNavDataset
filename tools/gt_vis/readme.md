# useful tools


## Read and Visualize the Ground Truth
The script loads all SPANCPT Ground True data and converts them to ENU frame or LiDAR local frame (set convert_body_frame = True) with the first line as origin. 

```bash
pip3 install numpy-quaternion matplotlib pymap3d

python3 run_vehicle_path.py 
```

<p align="center">
  <img width="712pix" src="img/vis_tst_gt.png">
</p>

## Acknowledgements
We make reference to the code from cadc_devkit(https://github.com/mpitropov/cadc_devkit)
