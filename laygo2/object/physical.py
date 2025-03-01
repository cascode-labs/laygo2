#!/usr/bin/python
########################################################################################################################
#
# Copyright (c) 2014, Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#   disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################################################################

"""
The physical module implements classes for various physical layout objects.
The types of objects supported are summarized below:

:obj:`PhysicalObject` - a base class for physical layout objects.

:obj:`IterablePhysicalObject` - a base class for iterable physical objects (eg. arrayed instances).

:obj:`PhysicalObjectGroup` - defines a group of physical objects.

:obj:`Rect` - defines a rect.

:obj:`Path` - defines a path.

:obj:`Pin` - defines a pin.

:obj:`Text` - defines a text label.

:obj:`Instance` - defines an instance.

:obj:`VirtualInstance` - defines a virtual instance composed of multiple physical objects.

"""

__author__ = "Jaeduk Han"
__maintainer__ = "Jaeduk Han"
__status__ = "Prototype"

import numpy as np
# from copy import deepcopy
import laygo2.util.transform as tf

class PhysicalObject:
    """
    The base class of physical layout objects, which has physical coordinate information.

    Notes
    -----
    * **Reference in Korean**: 물리 객체들의 기본 클래스, 물리적 좌표정보를 갖고 있다. 


    """

    def _get_xy(self):
        """numpy.ndarray(dtype=numpy.int): Get the x and y coordinate values of this object."""
        return self._xy


    def _set_xy(self, value):
        """numpy.ndarray(dtype=numpy.int): Set the x and y coordinate values of this object."""
        self._xy = np.asarray(value, dtype=np.int)
        self._update_pointers()


    name = None
    """str: The name of the object.

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
    >>> physical.name 
    “test”

    
    .. image:: ../assets/img/object_physical_PhysicalObject_name.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: Physical 객체의 이름.
    """


    _xy = np.zeros(2, dtype=np.int)
    """numpy.ndarray(dtype=numpy.int): The internal variable of xy."""


    xy = property(_get_xy, _set_xy)
    """numpy.ndarray: The physical coordinates [bottom_left, top_right] of the object.

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
    >>> physical.xy 
    [ [0,0], [200,200] ]

    
    .. image:: ../assets/img/object_physical_PhysicalObject_xy.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: Physical 객체의 좌표.
    """


    master = None
    """numpy.ndarray: The master of the current object (for array and pin objects).

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
    >>> physical.master
    None

    Notes
    -----
    **Reference in Korean**: Physical 객체의 master.
    """


    params = None
    """dict: The dictionary that contains the object parameters.

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params={maxI=0.005}) 
    >>> physical.params 
    {‘maxI’: 0.005 }

    Notes
    -----
    **Reference in Korean**: Physical 객체의 속성.
    """


    pointers = None
    """dict: The dictionary that contains major physical coordinates of the object. 
    Possible keys include left, right, top, bottom, bottom_left, center, etc.

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
    >>> physical.pointers 
    {'left': array([0, 100]), 'right': array([200, 100]),
     'bottom': array([100, 0]), 'top': array([100, 200]),
     'bottom_left': array([0, 0]), 'bottom_right': array([200, 0]),
     'top_left': array([0, 200]), 'top_right': array([200, 200]),
     ‘center’: array( [100, 100] ) 
    }

    .. image:: ../assets/img/object_physical_PhysicalObject_pointers.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: Physical 객체의 주요좌표들.
    """


    # Frequently used pointers
    left = None
    """numpy.ndarray: The left-center coordinate of the object.

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
    >>> physical.left
    [ 0, 100 ]

    
    .. image:: ../assets/img/object_physical_PhysicalObject_left.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: Physical 객체의 left pointer.
    """


    right = None
    """numpy.ndarray: The right-center coordinate of the object.

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
    >>> physical.right 
    [ 200, 100 ]

    
    .. image:: ../assets/img/object_physical_PhysicalObject_right.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: Physical 객체의 right pointer.
    """ 


    top = None
    """numpy.ndarray: The top-center coordinate of the object.

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
    >>> physical.top 
    [ 100, 200 ]

    
    .. image:: ../assets/img/object_physical_PhysicalObject_top.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: Physical 객체의 top pointer.
    """


    bottom = None
    """numpy.ndarray: The bottom-center coordinate of the object.

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
    >>> physical.bottom 
    [ 100, 0 ]

    
    .. image:: ../assets/img/object_physical_PhysicalObject_bottom.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: Physical 객체의 bottom pointer.
    """ 


    center = None
    """numpy.ndarray: The center-center coordinate of the object.

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
    >>> physical.center 
    [ 100, 100 ]

    
    .. image:: ../assets/img/object_physical_PhysicalObject_center.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: Physical 객체의 center pointer.
    """ 


    bottom_left = None 
    """numpy.ndarray: The bottom-left coordinate of the object.

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
    >>> physical.bottom_left 
    [ 0,0 ]

    
    .. image:: ../assets/img/object_physical_PhysicalObject_bottom_left.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: Physical 객체의 bottom_left pointer.
    """


    bottom_right = None
    """numpy.ndarray: The bottom-right coordinate of the object.

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
    >>> physical.bottom_right 
    [200, 0]

    
    .. image:: ../assets/img/object_physical_PhysicalObject_bottom_right.png 
      :height: 250

    Notes
    -----
    **Reference in Korean**: Physical 객체의 bottom_right pointer.
    """ 


    top_left = None
    """numpy.ndarray: The top-left coordinate of the object.

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
    >>> physical.top_left 
    [ 0, 200 ]

    
    .. image:: ../assets/img/object_physical_PhysicalObject_top_left.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: Physical 객체의 top_left pointer.
    """


    top_right = None
    """numpy.ndarray: The top-right coordinate of the object.

    Example
    --------
    >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
    >>> physical.top_right 
    [200, 200]

    
    .. image:: ../assets/img/object_physical_PhysicalObject_top_right.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: Physical 객체의 top_right pointer.
    """


    @property
    def bbox(self):
        """numpy.ndarray: The physical bounding box of the object.

        Example
        --------
        >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params=None) 
        >>> physical.xy 
        [ [0,0], [200,200] ]

        
        .. image:: ../assets/img/object_physical_PhysicalObject_bbox.png
          :height: 250
        
        Notes
        -----
        **Reference in Korean**: numpy.ndarray: Physical 객체의 bbox.
        """
        return np.sort(np.array([self.xy[0, :], self.xy[1, :]]), axis=0)

    def __init__(self, xy, name=None, params=None):
        """
        The constructor function of PhysicalObject class.

        Parameters
        ----------
        xy : numpy.ndarray
            physical coordinates of object, bbox.
        name : str
            object name.
        params : dict
            dictionary having attributes.

        Returns
        -------
        PhysicalObject

        Example
        --------
        >>> physical = object.physical.PhysicalObject( xy = [[0, 0], [200, 200]], name="test", params={'maxI’: 0.005}) 
        >>> print(physical) 
        <laygo2.object.physical.PhysicalObject object at 0x000001ECF0022948>
         name: test,
         class: PhysicalObject,
         xy: [[0, 0], [200, 200]],
         params: {'maxI': 0.005}
        
        
        Notes
        -----
        **Reference in Korean**:     PhysicalObject 클래스의 생성자 함수.

        파라미터

        xy(numpy.ndarray): 객체의 물리적 좌표, bbox

        name(str): 객체의 이름

        params(dict): 속성을 갖고 있는 Dictionary

        반환값

        laygo2.PhysicalObject

        """

        self.name = name
        # Initialize pointers.
        self.pointers = dict()
        self.pointers['left'] = np.array([0, 0], dtype=np.int)
        self.pointers['right'] = np.array([0, 0], dtype=np.int)
        self.pointers['bottom'] = np.array([0, 0], dtype=np.int)
        self.pointers['top'] = np.array([0, 0], dtype=np.int)
        self.pointers['bottom_left'] = np.array([0, 0], dtype=np.int)
        self.pointers['bottom_right'] = np.array([0, 0], dtype=np.int)
        self.pointers['top_left'] = np.array([0, 0], dtype=np.int)
        self.pointers['top_right'] = np.array([0, 0], dtype=np.int)
        self.left = self.pointers['left']
        self.right = self.pointers['right']
        self.bottom = self.pointers['bottom']
        self.top = self.pointers['top']
        self.bottom_left = self.pointers['bottom_left']
        self.bottom_right = self.pointers['bottom_right']
        self.top_left = self.pointers['top_left']
        self.top_right = self.pointers['top_right']

        self.params = params  # deepcopy(params)  # deepcopy increases the memory usage.
        self.xy = xy

    def __str__(self):
        """Return the summary of this object."""
        return self.summarize()

    def summarize(self):
        """Return the summary of this object."""
        name = 'None' if self.name is None else self.name
        return \
            self.__repr__() + " " \
            "\n    name: "   + name + ", " + \
            "\n    class: "  + self.__class__.__name__ + ", " + \
            "\n    xy: "     + str(self.xy.tolist()) + ", " + \
            "\n    params: " + str(self.params) + ", " 

    def _update_pointers(self):
        """Update pointers of this object. Called when the xy-coordinate of this object is updated."""
        xy_left = np.diag(np.dot(np.array([[1, 0], [0.5, 0.5]]), self.bbox)).astype(np.int)
        xy_right = np.diag(np.dot(np.array([[0, 1], [0.5, 0.5]]), self.bbox)).astype(np.int)
        xy_bottom = np.diag(np.dot(np.array([[0.5, 0.5], [1, 0]]), self.bbox)).astype(np.int)
        xy_top = np.diag(np.dot(np.array([[0.5, 0.5], [0, 1]]), self.bbox)).astype(np.int)
        xy_bottom_left = np.diag(np.dot(np.array([[1, 0], [1, 0]]), self.bbox)).astype(np.int)
        xy_bottom_right = np.diag(np.dot(np.array([[0, 1], [1, 0]]), self.bbox)).astype(np.int)
        xy_top_left = np.diag(np.dot(np.array([[1, 0], [0, 1]]), self.bbox)).astype(np.int)
        xy_top_right = np.diag(np.dot(np.array([[0, 1], [0, 1]]), self.bbox)).astype(np.int)
        xy_center    = np.diag(np.dot(np.array([[0.5, 0.5], [0.5, 0.5]]), self.bbox)).astype(np.int)
        self.pointers['left'] = xy_left
        self.pointers['right'] = xy_right
        self.pointers['bottom'] = xy_bottom
        self.pointers['top'] = xy_top
        self.pointers['bottom_left'] = xy_bottom_left
        self.pointers['bottom_right'] = xy_bottom_right
        self.pointers['top_left'] = xy_top_left
        self.pointers['top_right'] = xy_top_right
        self.pointers['center'] = xy_center
        self.left = self.pointers['left']
        self.right = self.pointers['right']
        self.bottom = self.pointers['bottom']
        self.top = self.pointers['top']
        self.bottom_left = self.pointers['bottom_left']
        self.bottom_right = self.pointers['bottom_right']
        self.top_left = self.pointers['top_left']
        self.top_right = self.pointers['top_right']
        self.center = self.pointers['center']


class IterablePhysicalObject(PhysicalObject):
    """
    Basic class of entities capable of iterable operation among physical entities.

    Notes
    -----
    **Reference in Korean**: 물리 객체들 중 iterable 연산이 가능한 객체들의 기본 클래스.

    """

    elements = None
    """
    numpy.ndarray: The numpy array that contains this object's subelements as its elements.

    Example
    --------
    >>> phy0 = physical.IterablePhysicalObject( xy=[[0, 0], [100, 100]], name="test" ) 
    >>> phy1 = physical.IterablePhysicalObject( xy=[[0, 0], [200, 200]], name="test") 
    >>> phy2 = physical.IterablePhysicalObject( xy=[[0, 0], [300, 300]], name="test") 
    >>> element = [phy0, phy1, phy2] 
    >>> iphy0 = physical.IterablePhysicalObject( xy=[[0, 0], [300, 300]], name="test", elements = element)
    >>> iphy0.elements 
    [physical.IterablePhysicalObject object,
     physical.IterablePhysicalObject object,
     physical.IterablePhysicalObject object ]

    Notes
    -----
    **Reference in Korean**: 객체의 하위 구성원.

    """
    def _get_xy(self):
        """numpy.ndarray(dtype=numpy.int): Get the x and y coordinate values of this object."""
        return self._xy

    def _set_xy(self, value):
        """numpy.ndarray(dtype=numpy.int): Set the x and y coordinate values of this object."""
        # Update the coordinate value of its elements.
        self._update_elements(xy_ofst=value - self.xy)
        # Update the coordinate value of the object itself.
        PhysicalObject._set_xy(self, value=value)

    xy = property(_get_xy, _set_xy)

    @property
    def shape(self):
        """The array dimension of this object.

        Example
        --------
        >>> phy0 = physical.IterablePhysicalObject( xy=[[0, 0], [100, 100]], name="test" ) 
        >>> phy1 = physical.IterablePhysicalObject( xy=[[0, 0], [200, 200]], name="test") 
        >>> phy2 = physical.IterablePhysicalObject( xy=[[0, 0], [300, 300]], name="test") 
        >>> element = [phy0, phy1, phy2] 
        >>> iphy0 = physical.IterablePhysicalObject( xy=[[0, 0], [300, 300]], name="test", elements = element)
        >>> iphy0.shape 
        [3]

        
        Notes
        -----
        **Reference in Korean**:     numpy.ndarray: 객체의 element의 shape.
        """
        if self.elements is None:
            return None
        else:
            return np.array(self.elements.shape, dtype=np.int)

    def __init__(self, xy, name=None, params=None, elements=None):
        """
        Constructor function of IterablePhysicalObject class.

        Parameters
        ----------
        xy : numpy.ndarray
            The physical coordinates [bottom_left,top_right] of the object.
        name : str
            The name of the object.
        params : dict
            The dictionary containing attributes of the object.
        elements : dict
            The dictionary containing element objects that compose the object.
        
        Returns
        -------
        laygo2.IterablePhysicalObject

        See Also
        --------
        Class PhysicalObject

        Example
        --------
        >>> phy0 = physical.IterablePhysicalObject( xy=[[0, 0], [100, 100]], name="test" ) 
        >>> phy1 = physical.IterablePhysicalObject( xy=[[0, 0], [200, 200]], name="test") 
        >>> phy2 = physical.IterablePhysicalObject( xy=[[0, 0], [300, 300]], name="test") 
        >>> element = [phy0, phy1, phy2] 
        >>> iphy0 = physical.IterablePhysicalObject( xy=[[0, 0], [300, 300]], name="test", elements = element)
        >>> print(iphy0) 
        <laygo2.object.physical.IterablePhysicalObject object at 0x0000013219648F08> 
        name: test, class: IterablePhysicalObject, 
        xy: [[0, 0], [300, 300]], params: None

        
        Notes
        -----
        **Reference in Korean**:     IterablePhysicalObject 클래스의 생성자 함수.

        파라미터

        xy(numpy.ndarray): 객체의 물리적 좌표, bbox

        name(str): 객체의 이름

        params(dict): 속성을 갖는 Dictionary

        elements(dict): 단위 객체를 갖는 Dictionary

        반환값

        laygo2.IterablePhysicalObject

        참조

        Class PhysicalObject
        """
        PhysicalObject.__init__(self, xy=xy, name=name, params=params)
        if elements is None:
            self.elements = None
        else:
            self.elements = np.asarray(elements)

    def __getitem__(self, pos):
        """Return the sub-elements of this object, based on the pos parameter."""
        return self.elements[pos]

    def __setitem__(self, pos, item):
        """Set the sub-elements of this object, based on the pos and item parameter. """
        self.elements[pos] = item

    def __iter__(self):
        """Iterator function. Directly mapped to the iterator of the elements attribute of this object."""
        return self.elements.__iter__()

    def __next__(self):
        """Iterator function. Directly mapped to the iterator of the elements attribute of this object."""
        return self.elements.__next__()

    def ndenumerate(self):
        """Enumerate over the element array. Calls np.ndenumerate() of the elements of this object."""
        return np.ndenumerate(self.elements)

    def _update_elements(self, xy_ofst):
        """Update xy-coordinates of this object's elements. An internal function for _set_xy()"""
        #print("aa?")
        if np.all(self.elements is not None):
            # Update the x and y coordinate values of elements.
            for n, e in self.ndenumerate():
                if e is not None:
                    e.xy = e.xy + xy_ofst

class PhysicalObjectGroup(IterablePhysicalObject):
    """
    A grouped physical object. Intended to be generated as a group in Virtuoso (not implemented yet).
    """
    # TODO: implement this.

    def summarize(self):
        """Return the summary of the object information."""
        return IterablePhysicalObject.summarize(self) + "\n" + \
               "  elements: " + str(self.elements)

    def __init__(self, xy, name=None, params=None, elements=None):
        """
        Constructor.

        Parameters
        ----------
        xy : numpy.ndarray(dtype=int)
            The coordinate of this object represented as a Numpy array [x, y].
        name : str, optional
            The name of the object.
        params : dict or None
            The dictionary that contains the parameters of this object, with parameter names as keys.
        elements : numpy.ndarray(dtype=LayoutObject) or None
            The iterable elements of the object.
        """
        IterablePhysicalObject.__init__(self, xy=xy, name=name, params=params, elements=elements)


'''
# Deprecated as PhysicalObjectGroup can be used instead in most cases.
# But the code is preserved for reference.
class PhysicalObjectArray(np.ndarray):
    """LayoutObject array class for containing multiple layout objects. Subclassing ndarray to utilize advance slicing
     functions."""
    name = None
    """str: the name of the object."""

    params = None
    """dict or None: parameters of the object. """

    _xy = None  # np.zeros(2, dtype=np.int)
    """numpy.ndarray(dtype=numpy.int): the internal variable of xy."""

    def get_xy(self):
        """numpy.ndarray(dtype=numpy.int): gets the x and y coordinate values of this object."""
        return self._xy

    def set_xy(self, value):
        """numpy.ndarray(dtype=numpy.int): sets the x and y coordinate values of this object."""
        if value is None:
            self._xy = value
        else:
            self._xy = np.asarray(value, dtype=np.int)

    xy = property(get_xy, set_xy)
    """numpy.ndarray(detype=numpy.int): the x and y coordinate values of the object."""

    def moveby(self, delta):
        """move the array and child objects by delta."""
        self.xy = self.xy + delta
        for i in self:
            i.xy = i.xy + delta

    def __new__(cls, input_array, name=None, xy=None, params=None):
        """
        Constructor for ndarray subclasses - check the NumPy manual for details.

        Parameters
        ----------
        input_array : np.ndarray
            An array of LayoutObject objects.
        name : str
            The name of the array.
        xy : numpy.ndarray(dtype=int)
            The xy-coordinate of the object. The format is [x0, y0].
        params : dict
            Additional parameters of the array.
        """
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # add the new attribute to the created instance
        obj.name = name
        obj.xy = None if xy is None else np.asarray(xy, dtype=np.int)
        obj.params = params
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        """
        Array finalizing function for subclassing ndarray - check the NumPy manual for details
        """
        if obj is None: return
        # Transfer parameters
        self.name = getattr(obj, 'name', None)
        self.xy = getattr(obj, 'xy', None)
        self.params = getattr(obj, 'params', None)

    def __str__(self):
        """Returns the summary of this object."""
        return self.summarize()

    def summarize(self):
        """Summarizes object information."""
        return "  " + \
               "name:" + self.name + ", " + \
               "class:" + self.__class__.__name__ + ", " + \
               "shape:" + str(self.shape) + ", " + \
               "xy:" + str(self.xy) + ", " + \
               "params:" + str(self.params) + "\n" + \
               "  elements:" + str(np.ndarray.__str__(self)) + "\n"
'''

class Rect(PhysicalObject):
    """
    Rectangle object class.

    Notes
    -----
    **Reference in Korean**: 사각형 객체 클래스.
    """

    layer = None
    """
    numpy.ndarray: The layer information [name, purpose] of the object.

    Example
    --------
    >>> rect0 = physical.Rect(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing’], netname='net0', hextension=20, vextension=20)
    >>> rect0.layer 
    [ ‘M1’, ‘drawing’ ]

    Notes
    -----
    **Reference in Korean**: 객체의 Layer 정보.
    """


    netname = None
    """
    str: The net name of the object.

    Example
    --------
    >>> rect0 = physical.Rect(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing’], netname='net0', hextension=20, vextension=20)
    >>> rect0.netname 
    “net0”
    
    Notes
    -----
    **Reference in Korean**: 객체의 노드명.
    """


    hextension = 0
    """
    int: The extension of the rect object in horizontal direction.

    Example
    --------
    >>> rect0 = physical.Rect(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing’], netname='net0', hextension=20, vextension=20)
    >>> rect0.hextension 
    20

    .. image:: ../assets/img/object_physical_rect_hextension.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: 객체의 수평방향으로의 확장값.
    """


    vextension = 0
    """
    int: The extension of the rect object in vertical direction.

    Example
    --------
    >>> rect0 = physical.Rect(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing’], netname='net0', hextension=20, vextension=20)
    >>> rect0.vextension 
    20

    .. image:: ../assets/img/object_physical_rect_vextension.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: 객체의 수직방향으로의 확장값.
    """


    color = None
    """
    int: The color (multi-patterning ID) parameter of the object.

    Example
    --------
    >>> rect0 = physical.Rect(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing’], netname='net0', hextension=20, vextension=20)
    >>> rect0.color 
    “notMPT”

    Notes
    -----
    **Reference in Korean**: 객체의 color.
    """

    @property
    def height(self):
        """
        int: The height of the object.

        Example
        --------
        >>> rect0 = physical.Rect(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing’], netname='net0', hextension=20, vextension=20)
        >>> rect0.height 
        100

        .. image:: ../assets/img/object_physical_rect_height.png
          :height: 250

        Notes
        -----
        **Reference in Korean**:     int: 객체의 높이.
        """
        return abs(self.xy[0, 1] - self.xy[1, 1])

    @property
    def width(self):
        """
        int: The width of the object.

        Example
        --------
        >>> rect0 = physical.Rect(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing’], netname='net0', hextension=20, vextension=20)
        >>> rect0.width 
        100
        
        .. image:: ../assets/img/object_physical_rect_width.png
          :height: 250

        Notes
        -----
        **Reference in Korean**:     int: 객체의 폭.
        """
        return abs(self.xy[0, 0] - self.xy[1, 0])

    @property
    def height_vec(self):
        """numpy.ndarray(dtype=int): The height vector [0, height]."""
        return np.array([0, self.height])

    @property
    def width_vec(self):
        """numpy.ndarray(dtype=int): The width vector [width, 0]."""
        return np.array([self.width, 0])

    @property
    def size(self):
        """
        numpy.ndarray: The size of the object.

        Example
        --------
        >>> rect0 = physical.Rect(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing’], netname='net0', hextension=20, vextension=20)
        >>> rect0.size 
        [100, 100]

        .. image:: ../assets/img/object_physical_rect_size.png
          :height: 250

        Notes
        -----
        **Reference in Korean**:     numpy.ndarray: 객체의 크기.
        """
        return np.array([self.width, self.height])

    def __init__(self, xy, layer, color=None, hextension=0, vextension=0, name=None, netname=None, params=None):
        """
        The constructor function.

        Parameters
        ----------
        xy : numpy.ndarray
            The physical coordinates [bottom_left, top_right] of the object.
        layer : list
            The layer information of the object.
        hextension : int
            The horizontal extension value of the object.
        vextension : int
            The vertical extension value of the object.
        name : str
            The name of the object.
        netname : str
            The net name of the object.
        params : dict
            The dictionary containing attributes of the object.
        color : str, optional.
            The coloring information of the object.
        
        Returns
        -------
        laygo2.Pin

        See Also
        --------
        Class PhysicalObject

        Example
        --------
        >>> rect0 = physical.Rect(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing’], netname='net0', hextension=20, vextension=20)
        >>> print( rect0 ) 
        <laygo2.object.physical.Rect object at 0x00000283542688C8> name: None, class: Rect, xy: [[0, 0], [100, 100]], params: None, , layer: ['M1', 'drawing'], netname: net0

        
        .. image:: ../assets/img/object_physical_rect_init.png
          :height: 250

        Notes
        -----
        **Reference in Korean**:     Rect 클래스의 생성자 함수

        파라미터

        xy(numpy.ndarray): 객체의 물리적 좌표, bbox

        layer(list): 객체의 layer 정보

        hextension(int): 객체의 수평부 확장값

        vextension(int): 객체의 수직 확장값

        name(str): 객체의 이름

        netname(str): 객체의 노드 명

        params(dict): 속성을 갖는 Dictionary [optional]

        color(str): 객체의 color [optional]

        반환값

        laygo2.Pin

        참조

        Class PhysicalObject
        """
        self.layer = layer
        if netname is None:
            self.netname = name
        else:
            self.netname = netname
        self.hextension = hextension
        self.vextension = vextension
        self.color = color
        PhysicalObject.__init__(self, xy=xy, name=name, params=params)


    def align(self, rect2):
        """
        Match the length of self and rect2 wires, when either width or height of the two objects is zero.

        Parameters
        ----------
        rect2 : Rect
            Rect which want to be matched
        """
        index = 0
        r0 = self
        r1 = rect2
        if r0.xy[0][0] == r0.xy[1][0]: # width is zero
                index = 1

        pnt = np.zeros([2, 2], dtype=int)
        pnt[0][1] = r0.bbox[1][index] # tr
        pnt[1][1] = r1.bbox[1][index] # tr
        pnt[0][0] = r0.bbox[0][index] # bl
        pnt[1][0] = r1.bbox[0][index] # bl

        if pnt[1][1] > pnt[0][1]:  # p1-top is upper then p0-top
            _xy = r0.bbox  # r0 correction
            _xy[1][index] = pnt[1][1]
            r0.xy = _xy
        elif pnt[1][1] < pnt[0][1]: #p1-top is lower then p0-top
            _xy = r1.bbox  # r1 correction
            _xy[1][index] = pnt[0][1]
            r1.xy = _xy

        if pnt[1][0] < pnt[0][0]:  # p1-bottom is lower then p0-bottom
            _xy = r0.bbox  # r0 correction
            _xy[0][index] = pnt[1][0]
            r0.xy = _xy
        elif pnt[1][0] > pnt[0][0]:
            _xy = r1.bbox  # r1 correction
            _xy[0][index] = pnt[0][0]
            r1.xy = _xy

    def summarize(self):
        """Return the summary of the object information."""
        return PhysicalObject.summarize(self) + ", " + \
                                              "layer: " + str(self.layer) + ", " + \
                                              "netname: " + str(self.netname)


class Path(PhysicalObject):
    """
    Path object class.

    Notes
    -----
    **Reference in Korean**: Path 객체 클래스.
    """
    # TODO: implement pointers.


    layer = None
    """
    list: The layer information [name, purpose] of object.
    
    Notes
    -----
    **Reference in Korean**: list: 객체의 레이어 정보.
    """


    netname = None
    """
    str: The net name of the object.

    Example
    --------
    >>> path0 = physical.Path(xy=[[0, 0], [0, 100]], width=10, extension=5, layer=['M1', 'drawing’], netname='net0’)
    >>> path0.netname 
    “net0”
    
    .. image:: ../assets/img/object_physical_path_netname.png 
      :height: 250

    Notes
    -----
    **Reference in Korean**: 객체의 노드명.
    """


    width = None
    """
    int: the width of the object.

    Example
    --------
    >>> path0 = physical.Path(xy=[[0, 0], [0, 100]], width=10, extension=5, layer=['M1', 'drawing’], netname='net0’)
    >>> path0.width 
    10

    .. image:: ../assets/img/object_physical_path_width.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: 객체의 폭.
    """


    extension = 0
    """
    int: The extension of the path object.

    Example
    --------
    >>> path0 = physical.Path(xy=[[0, 0], [0, 100]], width=10, extension=5, layer=['M1', 'drawing’], netname='net0’)
    >>> path0.extension 
    5
    
    .. image:: ../assets/img/object_physical_path_extension.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: 객체의 확장값.
    """

    @property
    def bbox(self):
        """The bounding box [bottom_left, top_right] information of the object."""
        return np.sort(np.array([self.xy[0], self.xy[-1]]), axis=0)

    def _update_pointers(self):
        """Update pointers of this object. Called when the value of xy of this object is updated."""
        pass

    def __init__(self, xy, layer, width, extension=0, name=None, netname=None, params=None):
        """
        The constructor function.

        Parameters
        ----------
        xy : numpy.ndarray
            The physical coordinates [bottom_left, top_right] of the object.
        layer : list
            The layer information of the object.
        width : int
            The width of the object.
        extension : int
            The extension value of the object.
        name : str
            The name of the object.
        netname : str
            The net name of the object.
        params : dict
            The dictionary containing attributes of the object.

        Returns
        -------
        numpy.ndarray

        See Also
        --------
        Class PhysicalObject

        Example
        --------
        >>> path0 = physical.Path(xy=[[0, 0], [0, 100]], width=10, extension=5, layer=['M1', 'drawing’], netname='net0’)
        >>> print( path0 ) 
        <laygo2.object.physical.Path object at 0x00000280D1F3CE88> name: None, class: Path, xy: [[0, 0], [0, 100]], params: None, width: 10, extension: 5, layer: ['M1', 'drawing'], netname: net0

        
        .. image:: ../assets/img/object_physical_path_init.png
          :height: 250

        Notes
        -----
        **Reference in Korean**:     Path 객체 생성

        파라미터

        xy(numpy.ndarray): 객체의 물리적 좌표, bbox

        layer(list): 객체의 layer 정보

        width(int): 객체의 폭

        extension(int): 객체의 확장값

        name(str): 객체의 이름

        netname(str): 객체의 노드 명

        params(dict): 속성을 갖는 Dictionary

        반환값

        numpy.ndarray

        참조

        Class PhysicalObject
        """
        self.layer = layer
        self.width = width
        self.extension = extension
        self.netname = netname
        PhysicalObject.__init__(self, xy=xy, name=name, params=params)
        self.pointers = dict()  # Pointers are invalid for Path objects.

    def summarize(self):
        """Return the summary of the object information."""
        return PhysicalObject.summarize(self) + ", " + \
               "width: " + str(self.width) + ", " + \
               "extension: " + str(self.extension) + ", " + \
               "layer: " + str(self.layer) + ", " + \
               "netname: " + str(self.netname)


class Pin(IterablePhysicalObject):
    """
    Pin object class.

    Notes
    -----
    **Reference in Korean**: Pin 객체 클래스.
    """

    layer = None
    """
    numpy.ndarray: The layer information of the object.

    Example
    --------
    >>> pin0 = physical.Pin(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing'], netname='net0', params={'direction': 'input'})path0.width
    >>> pin0.layer 
    ['M1', 'drawing']
    
    numpy.ndarray: 객체의 Layer 정보.
    """


    netname = None
    """
    str: The net name of the object.

    Example
    --------
    >>> pin0 = physical.Pin(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing'], netname='net0', params={'direction': 'input'})path0.width
    >>> pin0.netname 
    “net0”
    
    str: 객체의 노드명.
    """


    master = None
    """Instance: The master instance of the pin. Used for instance pins only."""

    @property
    def height(self):
        """
        int: The height of the object.

        Example
        --------
        >>> pin0 = physical.Pin(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing'], netname='net0', params={'direction': 'input'})path0.width
        >>> pin0.height 
        100
        
        Notes
        -----
        **Reference in Korean**:     int: 객체의 높이.
        """
        return abs(self.xy[0, 1] - self.xy[1, 1])

    @property
    def width(self):
        """
        int: The width of the object.

        Example
        --------
        >>> pin0 = physical.Pin(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing'], netname='net0', params={'direction': 'input'})path0.width
        >>> pin0.width 
        100
        
        Notes
        -----
        **Reference in Korean**:     int: 객체의 폭.
        """
        return abs(self.xy[0, 0] - self.xy[1, 0])

    @property
    def size(self):
        """
        numpy.ndarray: The size of the object.

        Example
        --------
        >>> pin0 = physical.Pin(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing'], netname='net0', params={'direction': 'input'})path0.width
        >>> pin0.size 
        [100, 100]
        
        Notes
        -----
        **Reference in Korean**:     numpy.ndarray: 객체의 크기.
        """
        return np.array([self.width, self.height])

    @property
    def height_vec(self):
        """numpy.ndarray(dtype=int): Return np.array([0, height])."""
        return np.array([0, self.height])

    @property
    def width_vec(self):
        """numpy.ndarray(dtype=int): Return np.array([width, 0])."""
        return np.array([self.width, 0])

    def __init__(self, xy, layer, name=None, netname=None, params=None, master=None, elements=None):
        """
        The constructor function of Pin class.

        Parameters
        ----------
        xy : numpy.ndarray
            The physical coordinates [bottom_left, top_right] of the object.
        layer : list
            The layer information of the object.
        name : str
            The name of the object.
        netname : str
            The net name of the object.
        params : dict
            The dictionary containing attributes of the object.
        
        Returns
        -------
        laygo2.Pin

        See Also
        --------
        Class IterablePhysicalObject

        Example
        --------
        >>> pin0 = physical.Pin(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing'], netname='net0', params={'direction': 'input'})path0.width
        >>> print( pin0 ) 
        <laygo2.object.physical.Pin object at 0x0000017DBDA4F508> name: None,
         class: Pin, xy: [[0, 0], [100, 100]], params: {'direction': 'input’},
         layer: ['M1', 'drawing'], netname: net0, shape: None, master: None

        
        Notes
        -----
        **Reference in Korean**:     Pin 클래스의 생성자 함수

        파라미터

        xy(numpy.ndarray): 객체의 물리적 좌표, bbox

        layer(list): 객체의 layer 정보

        name(str): 객체의 이름

        netname(str): 객체의 노드 명

        params(dict): 속성을 갖는 Dictionary

        반환값

        laygo2.Pin

        참조

        Class IterablePhysicalObject
        """
        self.layer = np.asarray(layer)
        if netname is None:
            netname = name
        self.netname = netname
        self.master = master
        IterablePhysicalObject.__init__(self, xy=xy, name=name, params=params, elements=elements)

    def summarize(self):
        """Return the summary of the object information."""
        return IterablePhysicalObject.summarize(self) + ", " + \
                                                      "layer: " + str(self.layer) + ", " + \
                                                      "netname: " + str(self.netname) + ", " + \
                                                      "shape: " + str(self.shape) + ", " + \
                                                      "master: " + str(self.master)

    def export_to_dict(self):
        db = dict()
        db['xy'] = self.xy.tolist()
        db['layer'] = self.layer.tolist()
        db['name'] = self.name
        db['netname'] = self.netname
        return db

class Text(PhysicalObject):
    """
    Text object class.

    Notes
    -----
    **Reference in Korean**: Text 객체 클래스.
    """
    layer = None
    """
    numpy.ndarray: Layer information of object.

    Example
    --------
    >>> text0 = physical.Text(xy=[[ 0, 0], [100,100 ]], layer=['text', 'drawing'], text='test', params=None)
    >>> text0.layer 
    ['text', 'drawing']

    Notes
    -----
    **Reference in Korean**: 객체의 Layer 정보.
    """


    text = None
    """
    str: Text content of object.

    Example
    --------
    >>> text0 = physical.Text(xy=[[ 0, 0], [100,100 ]], layer=['text', 'drawing'], text='test', params=None)
    >>> text0.text 
    ”text”
    
    Notes
    -----
    **Reference in Korean**: 객체의 텍스트 내용.
    """


    def __init__(self, xy, layer, text, name=None, params=None):
        """
        The constructor function of Text class.

        Parameters
        ----------
        xy : numpy.ndarray
            The physical coordinates [bottom_left, top_right] of the object.
        layer : list
            The layer information of the object.
        text : str
            The text content.
        name : str
            The name of the object.
        params : dict
            The dictionary containing attributes of the object.
        
        Returns
        -------
        laygo2.Text

        See Also
        --------
        Class PhysicalObject

        Example
        --------
        >>> pin0 = physical.Pin(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing'], netname='net0', params={'direction': 'input'})path0.width
        >>> pin0.text 
        [100, 100]

        
        Notes
        -----
        **Reference in Korean**:     Text 클래스의 생성자 함수

        파라미터

        xy(numpy.ndarray): 객체의 물리적 좌표, bbox

        layer(list): 객체의 layer 정보

        text(str): 텍스트 내용

        name(str): 객체의 이름

        params(dict): 속성을 갖는 Dictionary

        반환값

        laygo2.Text

        참조

        Class PhysicalObject
        """
        self.layer = layer
        self.text = text

        PhysicalObject.__init__(self, xy=xy, name=name, params=params)

    def summarize(self):
        """Return the summary of the object information."""
        return PhysicalObject.summarize(self) + \
                                              "\n    layer: " + str(self.layer) + ", " + \
                                              "\n    text: " + str(self.text)

class Instance(IterablePhysicalObject):
    """
    Instance object class.

    Notes
    -----
    **Reference in Korean**: Instance 객체 클래스.
    """
    # TODO: update (maybe) xy and sub-elements after transform property is updated.

    libname = None
    """
    str: The library name of the object.

    Example
    --------
    >>> inst0_pins = dict() 
    >>> inst0_pins[‘in’] = physical.Pin( xy = [[0, 0], [10,10]], layer = ['M1', 'drawing'], netname = 'in’) 
    >>> inst0_pins[‘out’]= physical.Pin( xy = [[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
    >>> inst0 = physical.Instance( name = "I0", xy = [ 100,100], libname="mylib", cellname="mycell", shape = [3,2], pitch = [200,200], unit_size = [100, 100], pins = inst0_pins , transform = 'R0’)
    >>> inst0.libname 
    mylib
    
    .. image:: ../assets/img/object_physical_instance_libname.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: 객체의 라이브러리 이름.
    """


    cellname = None
    """
    str: The cellname of the instance object.

    Example
    --------
    >>> inst0_pins = dict() 
    >>> inst0_pins[‘in’] = physical.Pin( xy = [[0, 0], [10,10]], layer = ['M1', 'drawing'], netname = 'in’) 
    >>> inst0_pins[‘out’]= physical.Pin( xy = [[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
    >>> inst0 = physical.Instance( name = "I0", xy = [ 100,100], libname="mylib", cellname="mycell", shape = [3,2], pitch = [200,200], unit_size = [100, 100], pins = inst0_pins , transform =  'R0’)
    >>> inst0.cellname
    mycell
    
    .. image:: ../assets/img/object_physical_instance_cellname.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: 객체가 속한 셀 이름.
    """

    viewname = None
    """str: The view name of the instance."""

    shape = None
    """np.array([int, int]) or None: The shape of the instance mosaic. None if the instance is non-mosaic."""

    _pitch = None
    """np.array([int, int]) or None: The internal variable for pitch."""

    unit_size = None
    """
    numpy.ndarray: Unit size when the object is constructed in array.

    Example
    --------
    >>> inst0_pins = dict() 
    >>> inst0_pins[‘in’] = physical.Pin( xy = [[0, 0], [10,10]], layer = ['M1', 'drawing'], netname = 'in’) 
    >>> inst0_pins[‘out’]= physical.Pin( xy = [[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
    >>> inst0 = physical.Instance( name = "I0", xy = [ 100,100], libname="mylib", cellname="mycell", shape = [3,2], pitch = [200,200], unit_size = [100, 100], pins = inst0_pins , transform =  'R0’)
    >>> inst0.unit_size 
    [100, 100]
    
    .. image:: ../assets/img/object_physical_instance_unit_size.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: 객체가 배열로 구성되었을 때 단위 크기.
    """


    transform = 'R0'
    """
    str: The transformation attribute of the object.

    Example
    --------
    >>> inst0_pins = dict() 
    >>> inst0_pins[‘in’] = physical.Pin( xy = [[0, 0], [10,10]], layer = ['M1', 'drawing'], netname = 'in’) 
    >>> inst0_pins[‘out’]= physical.Pin( xy = [[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
    >>> inst0 = physical.Instance( name = "I0", xy = [ 100,100], libname="mylib", cellname="mycell", shape = [3,2], pitch = [200,200], unit_size = [100, 100], pins = inst0_pins , transform =  'R0’)
    >>> inst0.transform 
    “R0”
    
    .. image:: ../assets/img/object_physical_instance_transform.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: 객체의 변환 속성.
    """


    pins = None
    """
    dict: The dictionary having the pins belonging to the object.

    Example
    --------
    >>> inst0_pins = dict() 
    >>> inst0_pins[‘in’] = physical.Pin( xy = [[0, 0], [10,10]], layer = ['M1', 'drawing'], netname = 'in’) 
    >>> inst0_pins[‘out’]= physical.Pin( xy = [[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
    >>> inst0 = physical.Instance( name = "I0", xy = [ 100,100], libname="mylib", cellname="mycell", shape = [3,2], pitch = [200,200], unit_size = [100, 100], pins = inst0_pins , transform =  'R0’)
    >>> inst0.pins 
    {'in': <laygo2.object.physical.Pin object at 0x000001CA76EE1348>, 'out': <laygo2.object.physical.Pin object at 0x000001CA7709BD48>} 
    >>> inst0.pins[“in”].shape 
    [3,2]
    >>> inst0.pins[“out”].shape 
    [3,2] 
    >>> inst0.pins[“in”][1,1].xy 
    [ [300, 300], [310, 310] ]
    
    .. image:: ../assets/img/object_physical_instance_pins.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: 객체에 속한 핀들을 갖는 Dict.
    """

    def _update_pins(self, xy_ofst):
        """Update xy-coordinates of this object's pins. An internal function for _set_xy()"""
        if self.pins is not None:
            for pn, p in self.pins.items():
                if np.all(p is not None):
                    # Update the x and y coordinate values of elements.
                    for n, e in np.ndenumerate(p):
                        if e is not None:
                            e.xy = e.xy + xy_ofst

    def _get_xy(self):
        """numpy.ndarray(dtype=numpy.int): Get the x and y coordinate values of this object."""
        return self._xy

    def _set_xy(self, value):
        """numpy.ndarray(dtype=numpy.int): Set the x and y coordinate values of this object."""
        # Update the coordinate value of its pins.
        self._update_pins(xy_ofst=value - self.xy)
        IterablePhysicalObject._set_xy(self, value=value)

    xy = property(_get_xy, _set_xy)

    @property
    def xy0(self):
        """
        numpy.ndarray: The coordinates of the primary corner of the object.

        Example
        --------
        >>> inst0_pins = dict() 
        >>> inst0_pins[‘in’] = physical.Pin( xy = [[0, 0], [10,10]], layer = ['M1', 'drawing'], netname = 'in’) 
        >>> inst0_pins[‘out’]= physical.Pin( xy = [[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
        >>> inst0 = physical.Instance( name = "I0", xy = [ 100,100], libname="mylib", cellname="mycell", shape = [3,2], pitch = [200,200], unit_size = [100, 100], pins = inst0_pins , transform =  'R0’)
        >>> inst0.xy0 
        [100, 100]

        .. image:: ../assets/img/object_physical_instance_xy0.png
          :height: 250

        Notes
        -----
        **Reference in Korean**:     numpy.ndarray: 객체의 주 코너 좌표.
        """
        return self.xy

    @property
    def xy1(self):
        """
        numpy.ndarray: The coordinates of the secondary corner of the object.

        Example
        --------
        >>> inst0_pins = dict() 
        >>> inst0_pins[‘in’] = physical.Pin( xy = [[0, 0], [10,10]], layer = ['M1', 'drawing'], netname = 'in’) 
        >>> inst0_pins[‘out’]= physical.Pin( xy = [[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
        >>> inst0 = physical.Instance( name = "I0", xy = [ 100,100], libname="mylib", cellname="mycell", shape = [3,2], pitch = [200,200], unit_size = [100, 100], pins = inst0_pins , transform =  'R0’)
        >>> inst0.xy1 
        [600, 400]
        
        .. image:: ../assets/img/object_physical_instance_xy1.png
          :height: 250

        Notes
        -----
        **Reference in Korean**:     numpy.ndarray: 객체의 보조 코너 좌표.
        """
        if self.size is None:
            return self.xy
        else:
            return self.xy + np.dot(self.size, tf.Mt(self.transform).T)

    @property
    def size(self):
        """
        numpy.ndarray: The size of the object.

        Example
        --------
        >>> inst0_pins = dict() 
        >>> inst0_pins[‘in’] = physical.Pin( xy = [[0, 0], [10,10]], layer = ['M1', 'drawing'], netname = 'in’) 
        >>> inst0_pins[‘out’]= physical.Pin( xy = [[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
        >>> inst0 = physical.Instance( name = "I0", xy = [ 100,100], libname="mylib", cellname="mycell", shape = [3,2], pitch = [200,200], unit_size = [100, 100], pins = inst0_pins , transform =  'R0’)
        >>> inst0.size 
        [500, 300]
        
        .. image:: ../assets/img/object_physical_instance_size.png
          :height: 250

        Notes
        -----
        **Reference in Korean**:     numpy.ndarray: 객체의 크기.
        """
        if self.shape is None:
            return self.unit_size
        else:
            return (self.shape - np.array([1, 1])) * self.pitch + self.unit_size

    def get_pitch(self):
        """numpy.ndarray(dtype=int): Get the pitch of the instance."""
        if self._pitch is None:
            return self.unit_size
        else:
            return self._pitch

    def set_pitch(self, value):
        """numpy.ndarray(dtype=int): Set the pitch of the instance."""
        self._pitch = value

    pitch = property(get_pitch, set_pitch)
    """
    numpy.ndarray: Pitch between unit object of the object in array.

    Example
    --------
    >>> inst0_pins = dict() 
    >>> inst0_pins[‘in’] = physical.Pin( xy = [[0, 0], [10,10]], layer = ['M1', 'drawing'], netname = 'in’) 
    >>> inst0_pins[‘out’]= physical.Pin( xy = [[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
    >>> inst0 = physical.Instance( name = "I0", xy = [ 100,100], libname="mylib", cellname="mycell", shape = [3,2], pitch = [200,200], unit_size = [100, 100], pins = inst0_pins , transform =  'R0’)
    >>> inst0.pitch 
    [200, 200]
    
    .. image:: ../assets/img/object_physical_instance_pitch.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: 배열로 구성된 객체의 단위객체간 간격.
    """

    def get_spacing(self):
        return self.pitch

    def set_spacing(self, value):
        self.pitch = value

    spacing = property(get_spacing, set_spacing)
    """
    numpy.ndarray: Spacing between unit object of the object in array.

    Example
    --------
    >>> inst0_pins = dict() 
    >>> inst0_pins[‘in’] = physical.Pin( xy = [[0, 0], [10,10]], layer = ['M1', 'drawing'], netname = 'in’) 
    >>> inst0_pins[‘out’]= physical.Pin( xy = [[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
    >>> inst0 = physical.Instance( name = "I0", xy = [ 100,100], libname="mylib", cellname="mycell", shape = [3,2], pitch = [200,200], unit_size = [100, 100], pins = inst0_pins , transform =  'R0’)
    >>> inst0.spacing 
    [200, 200]
    
    .. image:: ../assets/img/object_physical_instance_spacing.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: 배열로 구성된 객체의 단위객체간 간격.
    """

    @property
    def bbox(self):
        bbox = np.array([self.xy0, self.xy1])
        #return bbox
        #return self.xy + np.dot(self.size, tf.Mt(self.transform).T)
        return np.sort(bbox, axis=0)

    @property
    def height(self):
        """
        int: The height of the object.

        Example
        --------
        >>> inst0_pins = dict() 
        >>> inst0_pins[‘in’] = physical.Pin( xy = [[0, 0], [10,10]], layer = ['M1', 'drawing'], netname = 'in’) 
        >>> inst0_pins[‘out’]= physical.Pin( xy = [[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
        >>> inst0 = physical.Instance( name = "I0", xy = [ 100,100], libname="mylib", cellname="mycell", shape = [3,2], pitch = [200,200], unit_size = [100, 100], pins = inst0_pins , transform =  'R0’)
        >>> inst0.height 
        300
        
        .. image:: ../assets/img/object_physical_instance_height.png
          :height: 250

        Notes
        -----
        **Reference in Korean**:     int: 객체의 높이.
        """
        return abs(self.bbox[1][1] - self.bbox[0][1])

    @property
    def width(self):
        """
        int: The width of the object.

        Example
        --------
        >>> inst0_pins = dict() 
        >>> inst0_pins[‘in’] = physical.Pin( xy = [[0, 0], [10,10]], layer = ['M1', 'drawing'], netname = 'in’) 
        >>> inst0_pins[‘out’]= physical.Pin( xy = [[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
        >>> inst0 = physical.Instance( name = "I0", xy = [ 100,100], libname="mylib", cellname="mycell", shape = [3,2], pitch = [200,200], unit_size = [100, 100], pins = inst0_pins , transform =  'R0’)
        >>> inst0.width 
        500
        
        .. image:: ../assets/img/object_physical_instance_width.png
          :height: 250

        Notes
        -----
        **Reference in Korean**:     int: 객체의 폭.
        """
        return abs(self.bbox[1][0] - self.bbox[0][0])

    @property
    def height_vec(self):
        """numpy.ndarray(dtype=int): The height vector [0, height]."""
        return np.array([0, self.height])

    @property
    def width_vec(self):
        """numpy.ndarray(dtype=int): The width vector [width, 0]."""
        return np.array([self.width, 0])

    def __init__(self, xy, libname, cellname, viewname='layout', shape=None, pitch=None, transform='R0',
                 unit_size=np.array([0, 0]), pins=None, name=None, params=None):
        """
        The constructor function of Instance class.

        Parameters
        ----------
        xy : numpy.ndarray
            The primary coordinate [x0, y0] of the object.
        libname : str
            The library name of the object.
        cellname : str
            The cell name of the object.
        shape : numpy.ndarray
            The shape [col, row] of the elements.
        pitch : numpy.ndarray
            Pitch between the elements of the object in array.
        transform : str
            The transformation attribute of the object.
        unit_size : list
            Unit size of the object.
        pins : dict
            The dictionary containing pins belonging to the object.
        name : str
            The name of the object.
        params : dict
            The dictionary containing attributes of the object.
        
        Returns
        -------
        object (laygo2.Instance)

        See Also
        --------
        Class IterablePhysicalObject

        Example
        --------
        >>> inst0_pins = dict() 
        >>> inst0_pins[‘in’] = physical.Pin( xy = [[0, 0], [10,10]], layer = ['M1', 'drawing'], netname = 'in’) 
        >>> inst0_pins[‘out’]= physical.Pin( xy = [[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
        >>> inst0 = physical.Instance( name = "I0", xy = [ 100,100], libname="mylib", cellname="mycell", shape = [3,2], pitch = [200,200], unit_size = [100, 100], pins = inst0_pins , transform =  'R0’)
        >>> print( inst0[1,0].xy0 ) 
        [ 300, 100 ]

        .. image:: ../assets/img/object_physical_instance_init.png
          :height: 250

        Notes
        -----
        **Reference in Korean**:     Instance 클래스의 생성함수

        파라미터

        xy(numpy.ndarray): 객체의 주좌표 [x0, y0]

        libname(str): 객체의 library 이름

        cellname(str): 객체의 cell이름

        shape(numpy.ndarray): elements 의 shape, [column, row]

        pitch(numpy.ndarray): 배열로 구성된 객체의 하위객체간 간격

        transform(str): 객체의 변환 속성

        unit_size(list): 객체의 단위 크기

        pins(dict): 객체에 속한 핀들을 갖는 Dictionary

        name(str): 객체의 이름

        params(dict): 객체의 속성을 갖는 Dictionary

        반환값

        object (laygo2.Instance)

        참조

        Class IterablePhysicalObject
        """
        # Assign parameters.
        xy = np.asarray(xy)
        self.libname = libname
        self.cellname = cellname
        self.viewname = viewname
        if shape is not None:
            _shape = np.asarray(shape)
            if _shape.shape != (2, ):
                raise ValueError('Instance shape should be a (2, ) numpy array or None.')
            self.shape = _shape
        if pitch is not None:
            self.pitch = np.asarray(pitch)
        self.transform = transform
        self.unit_size = np.asarray(unit_size)

        # Construct an array for elements.
        if shape is None:
            # elements = self  # self-referencing causes recursion errors. Deprecated.
            elements = None
        else:
            _shape = tuple(shape)
            elements = np.zeros(_shape, dtype=np.object)
            # elements = LayoutObjectArray(np.zeros(_shape, dtype=np.object))
            _it = np.nditer(elements, flags=['multi_index', 'refs_ok'])
            while not _it.finished:
                _idx = _it.multi_index
                _xy = xy + np.dot(self.pitch * np.array(_idx), tf.Mt(self.transform).T)
                inst = Instance(xy=_xy, libname=libname, cellname=cellname, shape=None, pitch=pitch,
                                transform=self.transform, unit_size=self.unit_size, pins=pins, name=name, params=params)
                elements[_idx] = inst
                _it.iternext()

        IterablePhysicalObject.__init__(self, xy=xy, name=name, params=params, elements=elements)
        # Create the pin dictionary. Can we do the same thing without generating these many Pin objects?
        self.pins = dict()
        if pins is not None:
            if not isinstance(pins, dict):
                raise ValueError("The pins parameter for Instance objects should be a dictionary.")
            for pn, p in pins.items():
                _xy0 = xy + np.dot(p.xy, tf.Mt(transform).T)
                if shape is not None:
                    elements = []
                    for i in range(shape[0]):
                        elements.append([])
                        for j in range(shape[1]):
                            _xy = _xy0 + np.dot(self.pitch * np.array([i, j]), tf.Mt(transform).T)
                            # If p has elements, they need to be copied and transferred to the new pin.
                            _pelem = None
                            if p.elements is not None:
                                _pelem = np.empty(p.elements.shape, dtype=object)
                                for _idx, _pe in np.ndenumerate(p.elements):
                                    _pexy0 = xy + np.dot(_pe.xy, tf.Mt(transform).T) \
                                             + np.dot(self.pitch * np.array([i, j]), tf.Mt(transform).T)
                                    _pelem[_idx] = Pin(xy=_pexy0, netname=_pe.netname, layer=_pe.layer, name=_pe.name, master=self)
                            pin = Pin(xy=_xy, netname=p.netname, layer=p.layer, name=p.name, master=self,
                                      elements=_pelem)  # master uses self instead of self.elements[i, j].
                            elements[i].append(pin)
                    elements = np.array(elements)
                else:
                    # If p has elements, they need to be copied and transferred to the new pin.
                    _pelem = None
                    if p.elements is not None:
                        _pelem = np.empty(p.elements.shape, dtype=object)
                        for _idx, _pe in np.ndenumerate(p.elements):
                            _pexy0 = xy + np.dot(_pe.xy, tf.Mt(transform).T)
                            _pelem[_idx] = Pin(xy=_pexy0, netname=_pe.netname, layer=_pe.layer, name=_pe.name, master=self)
                    elements = _pelem
                self.pins[pn] = Pin(xy=_xy0, netname=p.netname, layer=p.layer, name=p.name, master=self,
                                    elements=elements)

    def summarize(self):
        """Summarize object information."""
        return PhysicalObject.summarize(self) + \
               "\n    size: " + str(self.size.tolist()) + \
               "\n    shape: " + str(None if self.shape is None else self.shape.tolist()) + \
               "\n    pitch: " + str(self.pitch.tolist()) + \
               "\n    transform: " + str(self.transform) + \
               "\n    pins: " + str(self.pins)

class VirtualInstance(Instance):  # IterablePhysicalObject):
    """
    VirtualInstance object class.

    Notes
    -----
    **Reference in Korean**: VirtualInstance 객체 클래스.
    """

    native_elements = None
    """
    dict: The dictionary containing physical entities constituting the object.

    Example
    --------
    >>> vinst0_pins = dict() 
    >>> vinst0_pins['in']  = physical.Pin(xy=[[0, 0], [10, 10]], layer=['M1', 'drawing'], netname='in') 
    >>> vinst0_pins['out'] = physical.Pin(xy=[[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out’)
    >>> vinst0_native_elements = dict() 
    >>> vinst0_native_elements['R0'] = physical.Rect(xy=[[0, 0], [10, 10]], layer=['M1', 'drawing']) 
    >>> vinst0_native_elements['R1'] = physical.Rect(xy=[[90, 90], [100, 100]], layer=['M1', 'drawing']) 
    >>> vinst0_native_elements['R2'] = physical.Rect(xy=[[0, 0], [100, 100]], layer=['prBoundary', 'drawing’])
    >>> vinst0 = physical.VirtualInstance(name='I0', libname='mylib', cellname='myvcell', xy=[500, 500], native_elements=vinst0_native_elements, shape=[3, 2], pitch=[100, 100], unit_size=[100, 100], pins=vinst0_pins, transform='R0’)
    >>> vinst0.native_elements 
    { ‘R0’ : physical.Rect, ‘R1’ : physical.Rect, ‘R2’ : physical.Rect }

    .. image:: ../assets/img/object_physical_VirtualInstance_native_elements.png
      :height: 250

    Notes
    -----
    **Reference in Korean**: 객체를 구성하는 물리객체들을 갖고있는 Dict.
    """
    # Dict[PhysicalObject] the elements that compose the virtual instance. Its keys represent the names of the elements.

    def __init__(self, xy, libname, cellname, native_elements, viewname='layout', shape=None, pitch=None,
                 transform='R0', unit_size=np.array([0, 0]), pins=None, name=None, params=None):
        """
        The constructor function of VirtualInstance class.

        Parameters
        ----------
        xy : numpy.ndarray
            The primary coordinate [x0, y0] of the object.
        libname : str
            The library name of the object.
        cellname : str
            The cell name of the object.
        native_elements : dict
            The dictionary containing physical entities constituting the object.
        shape : numpy.ndarray
            The shape [col, row] of the elements.
        pitch : numpy.ndarray
            Pitch between elements of the object in array.
        transform : str
            The transformation attribute of the object.
        unit_size : list
            Unit size of object.
        pins : dict
            The dictionary containing pins belonging to the object.
        name : str
            The name of the object.
        params : dict
            The dictionary containing attributes of the object.

        Returns
        -------
        object (laygo2.VirtualInstance)

        See Also
        --------
        Class Instance

        Example
        --------
        >>> vinst0 = physical.VirtualInstance(name='I0', libname='mylib', cellname='myvcell', xy=[500, 500], native_elements=vinst0_native_elements, shape=[3, 2], pitch=[100, 100], unit_size=[100, 100], pins=vinst0_pins, transform='R0’)
        >>> vinst0.native_elements 
        { ‘R0’ : physical.Rect, ‘R1’ : physical.Rect, ‘R2’ : physical.Rect }

        .. image:: ../assets/img/object_physical_VirtualInstance_init.png
          :height: 250

        Notes
        -----
        **Reference in Korean**:     VirtualInstance 클래스의 생성자 함수

        파라미터

        xy(numpy.ndarray): 객체의 주좌표 [x0, y0]

        libname(str): 객체의 library 이름

        cellname(str): 객체의 cell이름

        native_elements(dict): 객체를 구성하는 물리객체를 갖는 Dict

        shape(numpy.ndarray): elements 의 shape

        pitch(numpy.ndarray): 배열로 구성된 객체의 하위객체간 간격 

        transform(str): 객체의 변환 속성

        unit_size(list): 객체의 단위 크기

        pins(dict): 객체에 속한 핀들을 갖는 Dictionary

        name(str): 객체의 이름

        params(dict): 객체의 속성을 갖는 Dictionary

        반환값

        object (laygo2.VirtualInstance)

        참조

        Class Instance
        """
        self.native_elements = native_elements

        Instance.__init__(self, xy=xy, libname=libname, cellname=cellname, viewname=viewname, shape=shape, pitch=pitch,
                          transform=transform, unit_size=unit_size, pins=pins, name=name, params=params)

    def summarize(self):
        """Summarize object information."""
        return Instance.summarize(self) + "\n    native elements: " + str(self.native_elements)

    def get_element_position(self, obj ):
        """
        Get element's xy-position from origin.
        
        Parameters
        ----------
        obj : element
            element belongs to self
        """
        vinst = self
        tr    = vinst.transform
        coners = np.zeros((4, 2))
        v_r = np.zeros(2)  # for rotation
        bbox_raw = obj.bbox
        offset = vinst.xy
        if tr == "R0":
            v_r = v_r + (1, 1)
            coners[0] = offset + v_r * bbox_raw[0]
            coners[2] = offset + v_r * bbox_raw[1]
        elif tr == "MX":
            v_r = v_r + (1, -1)
            coners[1] = offset + v_r * bbox_raw[0]
            coners[3] = offset + v_r * bbox_raw[1]
            coners[0] = coners[0] + (coners[1][0], coners[3][1])
            coners[2] = coners[2] + (coners[3][0], coners[1][1])
        elif tr == "MY":
            v_r = v_r + (-1, 1)
            coners[3] = offset + v_r * bbox_raw[0]
            coners[1] = offset + v_r * bbox_raw[1]
            coners[0] = coners[0] + (coners[1][0], coners[3][1])
            coners[2] = coners[2] + (coners[3][0], coners[1][1])
        elif tr == "R90":
            v_r = v_r + (-1, -1)
            coners[2] = offset + v_r * bbox_raw[0]
            coners[0] = offset + v_r * bbox_raw[1]
        else:
            raise ValueError(" Others transfom not implemented")
        return coners[0], coners[2]








# Test
if __name__ == '__main__':
    test_rect = False
    test_path = False
    test_pin = False
    test_text = False
    test_pointer = False
    test_instance = True
    test_virtual_instance = False

    # You can create various objects by running part of the following commands.
    if test_rect:
        print("Rect test")
        rect0 = Rect(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing'], netname='net0', params={'maxI': 0.005})
        print(rect0)
    if test_path:
        print("Path test")
        path0 = Path(xy=[[0, 0], [0, 100]], width=10, extension=5, layer=['M1', 'drawing'], netname='net0')
        print(path0)
    if test_pin:
        print("Pin test")
        pin0 = Pin(xy=[[0, 0], [100, 100]], layer=['M1', 'drawing'], netname='net0', master=rect0,
                   params={'direction': 'input'})
        print(pin0)
    if test_text:
        print("Text test")
        text0 = Text(xy=[0, 0], layer=['text', 'drawing'], text='test', params=None)
        print(text0)
    if test_instance:
        print("Instance test - creating a vanilla instance.")
        inst0_pins = dict()
        inst0_pins['in'] = Pin(xy=[[0, 0], [10, 10]], layer=['M1', 'drawing'], netname='in')
        inst0_pins['out'] = Pin(xy=[[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out')
        inst0 = Instance(name='I0', xy=[100, 100], libname='mylib', cellname='mycell', shape=[3, 2], pitch=[100, 100],
                         unit_size=[100, 100], pins=inst0_pins, transform='R0')
        print("  ", inst0)
        print("  ", inst0.pointers)
        print(inst0.elements)
        for idx, it in inst0.ndenumerate():
            print("what?")
            print("  ", idx, it)
            print("  ", idx, it.pins['in'])
        print("Instance test - updating the instance's coordinate values.")
        inst0.xy = [200, 200]
        print("  ", inst0)
        print("  ", inst0.pointers)
        for idx, it in inst0.ndenumerate():
            print("  ", idx, it)
            print("  ", idx, it.pins['in'])
    if test_virtual_instance:
        print("VirtualInstance test - creating a vanilla virtual instance.")
        inst1_pins = dict()
        inst1_pins['in'] = Pin(xy=[[0, 0], [10, 10]], layer=['M1', 'drawing'], netname='in')
        inst1_pins['out'] = Pin(xy=[[90, 90], [100, 100]], layer=['M1', 'drawing'], netname='out')
        inst1_native_elements = dict()
        inst1_native_elements['R0'] = Rect(xy=[[0, 0], [10, 10]], layer=['M1', 'drawing'])
        inst1_native_elements['R1'] = Rect(xy=[[90, 90], [100, 100]], layer=['M1', 'drawing'])
        inst1_native_elements['R2'] = Rect(xy=[[0, 0], [100, 100]], layer=['prBoundary', 'drawing'])
        inst1 = VirtualInstance(name='I0', libname='mylib', cellname='myvcell', xy=[500, 500],
                                native_elements=inst1_native_elements, shape=[3, 2], pitch=[100, 100],
                                unit_size=[100, 100], pins=inst1_pins, transform='R0')
        print("  ", inst1)
        for idx, it in inst1.ndenumerate():
            print("  ", idx, it.pins['in'])
        for idx, it in inst1.pins['in'].ndenumerate():
            print("  ", idx, it)
