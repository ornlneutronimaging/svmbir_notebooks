import numpy as np
import warnings

def correct_alignment(unaligned_image, offsets, center=None, fill_gap=True, num_pix_unused=1, num_pix_neighbor=1):
    """Function to correct alignment of the 4 segments in each image caused by the mismatch between the 4 chips.
    
    Args:
        unaligned_image(ndarray): 3D projection data (height x width x wavelengths)
        offsets(list): a list of offset values along X and Y axis, respectively (X offset, Y offset)
        center(list,optional): X and Y coordinate of the center that is connected to all 4 chips
        fill_gap(bool,optional): true/false, the function will fill the gap after moving the chips according to the
            offsets if set to true
        num_pix_unused(int,optional): number of pixels along the border not to be used while filling the gap
        num_pix_neighbor(int,optional): number of neighboring pixels used for filling the gap
        
    Returns:
        ndarray: aligned projection data (height' x width' x wavelengths)
        """
    # Get the offsets
    x_offset = offsets[0]
    y_offset = offsets[1]

    # Get the center
    if center is not None:
        center_x = center[0]
        center_y = center[1]

        # Check if the unaligned image contains the alignment center along both axes
        if (center_x < 0) or (center_x > unaligned_image.shape[1]):
            center_x = unaligned_image.shape[1] // 2
            x_offset = 0
        if (center_y < 0) or (center_y > unaligned_image.shape[0]):
            center_y = unaligned_image.shape[0] // 2
            y_offset = 0

    else:
        center_x = unaligned_image.shape[1] // 2
        center_y = unaligned_image.shape[0] // 2

    # Return the original image if both the offset values are zero
    if (x_offset == 0) and (y_offset == 0):
        warning_message = "Alignment correction not performed as both the offset values are zero."
        warnings.warn(warning_message)

        return unaligned_image

    # Get the chips
    chip_1 = unaligned_image[:center_y, :center_x]
    chip_2 = unaligned_image[:center_y, center_x:]
    chip_3 = unaligned_image[center_y:, :center_x]
    chip_4 = unaligned_image[center_y:, center_x:]

    # Move the chips and create aligned image
    moved_image = np.zeros((unaligned_image.shape[0] + y_offset,
                            unaligned_image.shape[1] + x_offset,
                            unaligned_image.shape[2]))

    moved_image[:center_y, :center_x] = chip_1
    moved_image[:center_y, center_x + x_offset:] = chip_2
    moved_image[center_y + y_offset:, :center_x] = chip_3
    moved_image[center_y + y_offset:, center_x + x_offset:] = chip_4

    if fill_gap is True:
        num_wave = unaligned_image.shape[2]
        filled_image = np.copy(moved_image)

        # Fill gaps along y-axis
        if y_offset > 0:
            y_upper_bound = unaligned_image.shape[0] - num_pix_unused - num_pix_neighbor
            y_lower_bound = num_pix_unused + num_pix_neighbor
            if y_upper_bound > center_y >= y_lower_bound:
                y0_up = center_y - num_pix_unused - num_pix_neighbor
                y1_up = center_y - num_pix_unused
                region_up = np.expand_dims(np.mean(filled_image[y0_up:y1_up], axis=0), axis=0)

                y0_down = center_y + y_offset + num_pix_unused
                y1_down = center_y + y_offset + num_pix_unused + num_pix_neighbor
                region_down = np.expand_dims(np.mean(filled_image[y0_down:y1_down], axis=0), axis=0)

                weights_y = np.expand_dims(np.linspace(0, 1, y_offset + 2 * num_pix_unused), axis=1)

                for wave in range(num_wave):
                    filled_image[center_y - num_pix_unused:center_y + y_offset + num_pix_unused, :, wave] = \
                        weights_y[::-1] @ region_up[:, :, wave] + weights_y @ region_down[:, :, wave]

            else:
                warning_message = "Couldn't fill gaps along y-axis as the center is close to border."
                warnings.warn(warning_message)

        # Fill gaps along x-axis
        if x_offset > 0:
            x_upper_bound = unaligned_image.shape[1] - num_pix_unused - num_pix_neighbor
            x_lower_bound = num_pix_unused + num_pix_neighbor
            if x_upper_bound > center_x >= x_lower_bound:
                x0_left = center_x - num_pix_unused - num_pix_neighbor
                x1_left = center_x - num_pix_unused
                region_left = np.expand_dims(np.mean(filled_image[:, x0_left:x1_left], axis=1), axis=1)

                x0_right = center_x + x_offset + num_pix_unused
                x1_right = center_x + x_offset + num_pix_unused + num_pix_neighbor
                region_right = np.expand_dims(np.mean(filled_image[:, x0_right:x1_right], axis=1), axis=1)

                weights_x = np.expand_dims(np.linspace(0, 1, x_offset + 2 * num_pix_unused), axis=0)

                for wave in range(num_wave):
                    filled_image[:, center_x - num_pix_unused:center_x + x_offset + num_pix_unused, wave] = \
                        region_left[:, :, wave] @ weights_x[:, ::-1] + region_right[:, :, wave] @ weights_x

            else:
                warning_message = "Couldn't fill gaps along x-axis as the center is close to border."
                warnings.warn(warning_message)

        return filled_image

    else:
        return moved_image