from module.image_preprocessing import ImagePreprocessing
from module.camera_realsense import CameraRealsense
import module.helper as helper
import module.convert as convert
import cv2 as cv
import numpy as np
import copy


helper.print_log("Bat dau chay chuong trinh lay points")
if __name__ == "__main__":
    try:
        camera = CameraRealsense(enable_color=True, enable_depth=False)
        color_image, depth_image  = camera.get_image() 
        # color_image = cv.imread("./test.png", cv.IMREAD_COLOR)
        if color_image is None:
            helper.print_log('Khong ton tai color image. Kiem tra lai camera')
        else:
            img_process = ImagePreprocessing()
            mask = img_process.fitler_mask(source_image=color_image)
            array_point = img_process.find_contours(mask=mask)
            cropped_img = img_process.crop_image(array_point=array_point, source_image=color_image)
            cropped_img_gray, threshold_image = img_process.thresholding(mask = mask, cropped_image=cropped_img)
            morph_image = img_process.morphology_processing(threshold_image=threshold_image)
            edge = img_process.canny_detect(morph_image=morph_image)
            corners, draw_lines = img_process.hough_detect(edge=edge)
            corners = np.asanyarray(corners)
            # get depth value
            depth = helper.get_transfer_data('depth')
            img_result_red = cv.bitwise_and(color_image, color_image, mask=mask)
            hough_img = copy.copy(color_image)
            for line in draw_lines:
                for x1,y1,x2,y2 in line:
                    cv.line(hough_img,(x1,y1),(x2,y2),(255,0,0),5)

            # Show ket qua
            if helper.get_config('show_results') is True:
                cv.imshow("Source Color Image", color_image)
                # show ket qua loc vung  mau do
                cv.imshow("Red Mask Filter Result", img_result_red)        
                # # show ket qua tim contour vung mau do (cho qua trinh cat anh)
                # contour_red_img = color_image
                # cv.imshow("Contour of Red Area", contour_red_img)
                # show ket qua crop vung anh
                cv.imshow("Cropped Image", cropped_img)
                # show ket qua gray scale va thresholding
                cv.imshow("Grayscale Image", cropped_img_gray)
                cv.imshow("Thresholding Image", threshold_image)
                # show ket qua xu ly hinh thai hoc (bang phuong phap opening)
                cv.imshow("Morphology Processing (Opening)", morph_image)
                # show ket qua xu ly canh bang Canny
                cv.imshow("Canny Detection", edge)
                # show ket qua xu ly tim canh bang Hough Transform, corner se la final result
                cv.imshow('Hough Line result', hough_img)
                # cv.waitKey()
            if helper.get_config('save_image_each_step') is True:
                cv.imwrite(helper.get_config('image_input'), color_image)
                cv.imwrite(helper.get_config('image_mask_red'), img_result_red)
                
                cv.imwrite(helper.get_config('image_croped'), cropped_img)
                cv.imwrite(helper.get_config('image_grayscale'), cropped_img_gray)
                cv.imwrite(helper.get_config('image_threshold'), threshold_image)
                cv.imwrite(helper.get_config('image_opening'), morph_image)
                cv.imwrite(helper.get_config('image_canny'), edge)
                cv.imwrite(helper.get_config('image_hough_line'), hough_img)


            # ghi lai bien rotate image
            rotate_source_img = copy.copy(color_image)
            img_with_point = copy.copy(color_image)
            # draw and save result
            i = 0
            for corner in corners:
                i = i + 1
                name = 'corner_' + (str)(i)
                color = helper.get_corner_color(name)
                # helper.print_log(str(corner))
                # helper.set_transfer_data(name, corner.tolist())
                color_image = helper.draw_point_to_image(point=corner, source_image=color_image, color=color)
                img_with_point = helper.draw_point_to_image(point=corner, source_image=img_with_point, color=color)

                color_image = helper.put_text_to_image(point=corner, source_image=color_image, text=str(i), text_size=1)
                point_text = "(" + "{:.2f}".format(corner[0]) + ", " + "{:.2f}".format(corner[1]) + ")"
                img_with_point = helper.put_text_to_image(point=corner, source_image=img_with_point, text=point_text, text_size=1)

                world_point = convert.pixel_to_point(corner[0], corner[1], depth)
                helper.save_pixel_and_point(name, corner.tolist(), world_point)
            # lay anh rotate de hien thi ra giao dien
            rotate_image = helper.get_rotate_result_image(rotate_source_img, corners)
            # save result image
            cv.imwrite(helper.get_config('image_corner'), color_image)
            cv.imwrite(helper.get_config('image_rotate_final'), rotate_image)

            cv.imwrite(helper.get_config('image_with_point'), img_with_point)

            if helper.get_config('show_results') is True:
                cv.imshow("Final Result", color_image)
                cv.imshow("Rotate Result Image", rotate_image)
                cv.waitKey()
            # mo giao dien
            import module.my_app as my_app
            my_app.run_app()
    except Exception as e:   
        helper.print_log('Co loi xay ra trong get_points.py')
        helper.print_log(str(e))