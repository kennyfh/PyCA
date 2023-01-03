#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Module: Pixel Perfect Polygon Hitbox
# Created By  : TEODORO JIMÉNEZ LEPE
#               KENNY JESÚS FLORES HUAMÁN
# version ='1.0'
# ---------------------------------------------------------------------------
# This file contains a functions to generate polygon hitbox
# ---------------------------------------------------------------------------

# IMPORTS

# Third-party imports
import numpy as np
from typing import List,Tuple




def ordered_vertices(vertices: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Given a list of vertices in any order, this function returns the vertices in
    a clockwise order.

    Args:
        vertices (list[tuple[float,float]]): List of vertices to be sorted in clockwise order.

    Returns:
        list[tuple[float,float]]: List of sorted vertices in clockwise order.

"""
    angle = np.zeros([1,len(vertices)])

    center_x = np.average(list(zip(*vertices))[0])
    center_y = np.average(list(zip(*vertices))[1])
    center = np.array([center_x,center_y])
    #unit_reference_vector = np.array([0,1])
    #unit_reference_vector = (np.array(vertices[0]) - center)/np.linalg.norm(center - np.array(vertices[0]))
    k = 0
    for i,j in vertices:
        
        unit_vector_to_center = (np.array([i,j]) - center)/np.linalg.norm(center - np.array([i,j]))
        #print(np.dot(unit_vector_to_center,unit_reference_vector))
        
        #angle[0,k] = np.arccos(np.dot(unit_vector_to_center,unit_reference_vector))
        angle[0,k] = np.arccos(unit_vector_to_center[1])
        
        if i < center[0]:
            angle[0,k] = 2*np.pi - angle[0,k]
        
        k = k + 1
    
    angle = angle*180/np.pi
    # print(angle.tolist()[0])
    # print(vertices)
    # print(center)

    ordered_vertices = [x for _, x in sorted(zip(angle.tolist()[0], vertices), key=lambda pair: pair[0])]
    #Z = [x for _, x in sorted(zip(Y,X))]
    #Z = [x for _, x in sorted(zip(Y, X), key=lambda pair: pair[0])]
    return ordered_vertices #list of tuples

def is_in_polygon(point: Tuple[float, float], ordered_vertices: List[Tuple[float, float]]) -> bool:
    """
    Check if the given `point` is inside the polygon defined by `ordered_vertices`.

    Args:
    - point: A tuple of integers representing the x and y coordinates of the point.
    - ordered_vertices: A list of tuples of integers representing the vertices of the polygon, in clockwise order.

    Returns:
    - A boolean indicating if the point is inside the polygon or not.

    Example:
    >>> is_in_polygon((0, 0), [(0, 0), (0, 1), (1, 1), (1, 0)])
    True
    >>> is_in_polygon((2, 2), [(0, 0), (0, 1), (1, 1), (1, 0)])
    False
    """
    positive_cross_products = 0 
    
    for i in range(len(ordered_vertices)):
        if i != len(ordered_vertices) - 1:
            vertex_to_point = np.array(point) - np.array(ordered_vertices[i])
            vertex_to_next_vertex = np.array(ordered_vertices[i+1]) - np.array(ordered_vertices[i])
            
            vertex_to_point = np.insert(vertex_to_point,2,0)
            vertex_to_next_vertex = np.insert(vertex_to_next_vertex,2,0)
            cross_product_z = np.cross(vertex_to_point, vertex_to_next_vertex)[2]
            
            if cross_product_z > 0:
                positive_cross_products = positive_cross_products + 1
                
        else: 
            vertex_to_point = np.array(point) - np.array(ordered_vertices[i])
            vertex_to_next_vertex = np.array(ordered_vertices[0]) - np.array(ordered_vertices[i])
            
            vertex_to_point = np.insert(vertex_to_point,2,0)
            vertex_to_next_vertex = np.insert(vertex_to_next_vertex,2,0)
            cross_product_z = np.cross(vertex_to_point, vertex_to_next_vertex)[2]
            
            if cross_product_z > 0:
                positive_cross_products = positive_cross_products + 1
    #print(positive_cross_products)            
    if positive_cross_products == len(ordered_vertices):
        return True
    else:
        return False
    
    