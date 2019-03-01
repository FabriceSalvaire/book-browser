####################################################################################################
#
# BookBrowser - A Digitised Book Solution
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

"""Module to implement an image filter pipeline.  Largely inspired from `ITK <https://itk.org>`_.

Call Diagram:

.. code::

    <ImageFilter>.update()
        <ImageFilter>.output().update()

            <ImageFilterOutput>.update_output_information()
                <ImageFilter source>.update_output_information()
                    for each input:
                        input.update_output_information()
                    <ImageFilter>.generate_output_information()
                        for each output:
                            image_format = self.generate_image_format(output) [FILTER WORK]
                            output.copy_information(image_format)
                                <ImageFilterOutput>.image = Image(image_format)

            <ImageFilterOutput>.update_output_data()
                <ImageFilter source>.update_output_data() if outdated
                    for each input:
                        input.update_output_data()
                    <ImageFilter>.generate_data() [FILTER WORK]
                    for each output:
                        output.data_has_been_generated()
                            update timestamp

"""

__all__ = [
    'ImageFilter',
]

####################################################################################################

import logging

from BookBrowser.Common.TimeStamp import TimeStamp, TimeStampMixin
from ..Image import Image

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

# LargestPossibleRegion — the image in its entirety.
# BufferedRegion — the portion of the image retained in memory.
# RequestedRegion — the portion of the region requested by a filter or other class when operating on the image.

####################################################################################################

# DataObject

class ImageFilterOutput(TimeStampMixin):

    """Class to implement an image filter output"""

    _logger = _module_logger.getChild('ImageFilterOutput')

    ##############################################

    def __init__(self, source, name):

        # When was this data last generated?
        # This time stamp is an integer number and it is intended to synchronize the activities of
        # the pipeline. It doesn't relates to the clock time of acquiring or processing the data.
        super().__init__()

        # The maximum modification time of all upstream filters and outputs.
        # This does not include the modification time of this output.
        self._pipeline_time = 0

        self.connect_source(source, name)

        self.image = None
        # self._image_format = None

    ##############################################

    @property
    def source(self):
        return self._source

    ##############################################

    @property
    def name(self):
        return "{}.{}".format(self._source.name, self._name)

    ##############################################

    @property
    def pipeline_time(self):
        return self._pipeline_time

    @pipeline_time.setter
    def pipeline_time(self, time):
        self._pipeline_time = time

    ##############################################

    # @property
    # def image(self):
    #     return self._image

    ##############################################

    @property
    def image_format(self):

        if self.image is not None:
            return self.image.image_format
        else:
            return None
        # return self._image_format

    ##############################################

    def connect_source(self, source, name):

        self._source = source # image_filter
        self._name = name
        self.modified()

    ##############################################

    def disconnect_source(self):

        self._source = None
        self._name = None
        self.modified()

    ##############################################

    def update(self):

        # Provides opportunity for the data object to insure internal consistency before
        # access. Also causes owning source/filter (if any) to update itself. The Update() method is
        # composed of UpdateOutputInformation(), PropagateRequestedRegion(), and
        # UpdateOutputData(). This method may call methods that throw an InvalidRequestedRegionError
        # exception. This exception will leave the pipeline in an inconsistent state. You will need
        # to call ResetPipeline() on the last ProcessObjectWithTimeStamp in your pipeline in order
        # to restore the pipeline to a state where you can call Update() again.

        self._logger.info(self.name)
        self.update_output_information()
        #!# self.propagate_requested_region()
        self.update_output_data()

    ##############################################

    def update_output_information(self):

        # Update the information for this DataObjectWithTimeStamp so that it can be used as an
        # output of a ProcessObjectWithTimeStamp. This method is used in the pipeline mechanism to
        # propagate information and initialize the meta data associated with a
        # DataObjectWithTimeStamp. Any implementation of this method in a derived class is assumed
        # to call its source's ProcessObjectWithTimeStamp::UpdateOutputInformation() which
        # determines modified times, LargestPossibleRegions, and any extra meta data like spacing,
        # origin, etc. Default implementation simply call's it's source's UpdateOutputInformation().

        self._logger.info(self.name)
        self._source.update_output_information()

    ##############################################

    def propagate_requested_region(self):

        # Methods to update the pipeline. Called internally by the pipeline mechanism. 

        self._logger.info(self.name)

        # If we need to update due to pipeline modification time, or the fact that our data was
        # released, then propagate the update region to the source if there is one.
        if self.modified_time < self._pipeline_time:
            self._source.propagate_requested_region(self)

        # Check that the requested region lies within the largest possible region
        # self.verify_requested_region()

    ##############################################

    def update_output_data(self):

        self._logger.info(self.name)

        # If we need to update due to pipeline modification time, or the fact that our data was
        # released, then propagate the UpdateOutputData to the source if there is one.
        if self.modified_time < self._pipeline_time:
            self._source.update_output_data()

    ##############################################

    def copy_information(self, image_format):

        # was input_

        # Copy information from the specified data set. This method is part of the pipeline
        # execution model. By default, a ProcessObjectWithTimeStamp will copy meta-data from the
        # first input to all of its outputs. See
        # ProcessObjectWithTimeStamp::GenerateOutputInformation(). Each subclass of
        # DataObjectWithTimeStamp is responsible for being able to copy whatever meta-data it needs
        # from from another DataObjectWithTimeStamp. The default implementation of this method is
        # empty. If a subclass overrides this method, it should always call its superclass' version.

        # self._logger.info("from {} to {}\n{}".format(input_.name, self.name,
        #                                              str(input_.image_format)))

        self._logger.info("Make output for {} with shape \n{}".format(
            self.name,
            str(image_format),
        ))
        self.image = Image(image_format)

    ##############################################

    def data_has_been_generated(self):

        self._logger.info(self.name)
        self.modified()

####################################################################################################

class ImageFilter(TimeStampMixin):

    """Class to implement an image filter"""

    # These attributes must be defined in subclasses
    __filter_name__ = None # a string to identify the filter
    __input_names__ = None # list of input's name
    __output_names__ = None # list of output's name

    _last_filter_id = 0

    _logger = _module_logger.getChild('ImageFilter')

    ##############################################

    @classmethod
    def _new_filter_id(cls):
        cls._last_filter_id += 1
        return cls._last_filter_id

    ##############################################

    def __init__(self):

        super().__init__()

        self._filter_id = self._new_filter_id() # Fixme: purpose ???

        # Time when generate_output_information was last called.
        self._output_information_time = TimeStamp() # Fixme: versus mixin ???

        # This flag indicates when the pipeline is executing.
        # It prevents infinite recursion when pipelines have loops.
        self._updating = False

        self._inputs = dict()
        self._outputs = {name:ImageFilterOutput(self, name) for name in self.__output_names__}

        self.modified()

    ##############################################

    def __del__(self):
        for output in self._outputs.values():
            output.disconnect_source()

    ##############################################

    def __repr__(self):
        return self.__filter_name__

    ##############################################

    @property
    def name(self):
        return self.__filter_name__

    @property
    def filter_id(self):
        return self._filter_id

    @property
    def input_names(self):
        return self.__input_names__

    @property
    def output_names(self):
        return self.__output_names__

    ##############################################

    def input(self, name=None):
        if name is None:
            name = self.__input_names__[0]
        return self._inputs[name]

    ##############################################

    def connect_input(self, source, name=None):
        """Connect the source filter to the named input"""
        if name is None:
            name = self.__input_names__[0]
        self._inputs[name] = source

    ##############################################

    @classmethod
    def connect_filters(cls, filters):

        for i in range(1, len(filters)):
            in_filter = filters[i-1]
            out_filter = filters[i]
            out_filter.connect_input(in_filter.output())

        return filters[-1]

    ##############################################

    def disconnect_input(self, name):
        if name in self._inputs:
            del self._inputs[name]

    ##############################################

    def output(self, name=None):
        if name is None:
            name = self.__output_names__[0]
        return self._outputs[name]

    ##############################################

    def update(self):
        """Update the filter output

        Call this method to generate data through the pipeline.
        """
        self._logger.info(self.name)
        self.output().update()

    ##############################################

    def update_output_information(self):

        self._logger.info(self.name)

        # Watch out for loops in the pipeline
        if self._updating:
            self._logger.info("{} is updating!".format(self.name))
            # Since we are in a loop, we will want to update. But if we don't modify this filter,
            # then we will not execute because our output information modification time will be more
            # recent than the modification time of our output.
            self.modified()
            return

        # Verify that the process object has been configured correctly, that all required inputs are
        # set, and needed parameters are set appropriately before we continue the pipeline, i.e. is
        # the filter in a state that it can be run.
        # self.verify_preconditions()
        for input_name in self.__input_names__:
            if input_name not in self._inputs:
                raise NameError("Input {} is required".format(input_name))

        # We now wish to set the pipeline modification time of each output to the largest of this
        # filter's modification time, all input's pipeline modification time, and all input's
        # modification time.  We begin with the modification time of this filter.
        modified_time = self.modified_time

        # Loop through the inputs
        for input_ in self._inputs.values():
            # Propagate the update output information call
            self._updating = True
            input_.update_output_information()
            self._updating = False

            # What is the pipeline modification time of this input? Compare this against our current
            # computation to find the largest one.  Pipeline modification time of the input does not
            # include the modification time of the data object itself. Factor these modification
            # times into the next pipeline modification time
            modified_time = max(modified_time, input_.modified_time, input_.pipeline_time)

        # Call generate_output_information for subclass specific information.  Since
        # update_output_information propagates all the way up the pipeline, we need to be careful
        # here to call generate_output_information only if necessary. Otherwise, we may cause this
        # source to be modified which will cause it to execute again on the next update.
        if modified_time > int(self._output_information_time):
            for output in self._outputs.values():
                output.pipeline_time = modified_time

            # Verify that all the inputs are consistent with the requirements of the filter. For
            # example, subclasses might want to ensure all the inputs are in the same coordinate
            # frame.
            # self.verify_input_information()

            # Finally, generate the output information.
            self.generate_output_information()

            # Keep track of the last time GenerateOutputInformation() was called
            self._output_information_time.modified()

    ##############################################

    def generate_output_information(self):

        # Generate the information describing the output data. The default implementation of this
        # method will copy information from the input to the output. A filter may override this
        # method if its output will have different information than its input. For instance, a
        # filter that shrinks an image will need to provide an implementation for this method that
        # changes the spacing of the pixels. Such filters should call their superclass'
        # implementation of this method prior to changing the information values they need
        # (i.e. GenerateOutputInformation() should call Superclass::GenerateOutputInformation()
        # prior to changing the information.

        self._logger.info(self.name)

        # if self._inputs:
        #     primary_input = self.input()
        #     for output in self._outputs.values():
        #         output.copy_information(primary_input)

        if self._inputs:
            for output in self._outputs.values():
                image_format = self.generate_image_format(output)
                output.copy_information(image_format)

    ##############################################

    def propagate_requested_region(self, output):

        # Send the requested region information back up the pipeline (to the filters that precede this one).

        self._logger.info(self.name)

        # check flag to avoid executing forever if there is a loop
        if self._updating:
            self._logger.info("{} is updating!".format(self.name))
            return

        # Give the subclass a chance to indicate that it will provide more data then required for
        # the output. This can happen, for example, when a source can only produce the whole output.
        # Although this is being called for a specific output, the source may need to enlarge all
        # outputs.
        # self.enlarge_output_requested_region(output)

        # Give the subclass a chance to define how to set the requested regions for each of its
        # outputs, given this output's requested region.  The default implementation is to make all
        # the output requested regions the same.  A subclass may need to override this method if
        # each output is a different resolution.
        # self.generate_output_requested_region(output)

        # Give the subclass a chance to request a larger requested region on the inputs. This is
        # necessary when, for example, a filter requires more data at the "internal" boundaries to
        # produce the boundary values - such as an image filter that derives a new pixel value by
        # applying some operation to a neighborhood of surrounding original values.
        # self.generate_input_requested_region()

        # Now that we know the input requested region, propagate this through all the inputs.
        self._updating = False # Fixme: ok ???
        for input_ in self._inputs.values():
            input_.propagate_requested_region()
        self._updating = False

    ##############################################

    def update_output_data(self):

        self._logger.info(self.name)

        # prevent chasing our tail
        if self._updating:
            self._logger.info("{} is updating!".format(self.name))
            return

        # Prepare all the outputs. This may deallocate previous bulk data.
        # self.prepare_outputs()

        # Propagate the update call - make sure everything we might rely on is up-to-date
        # Must call PropagateRequestedRegion before UpdateOutputData if multiple inputs since they
        # may lead back to the same data object.
        self._updating = True
        if len(self._inputs) == 1:
            self.input().update_output_data()
        else:
            for input_ in self._inputs.values():
                input_.propagate_requested_region()
                input_.update_output_data()

        # start
        self.generate_data()
        # stop

        # Now we have to mark the data as up to date.
        for output in self._outputs.values():
            output.data_has_been_generated()

        self._updating = False

    ##############################################

    def generate_image_format(self, output):

        """Method to generate the image format.

        Must be overridden in subclass is output format is different.
        """

        return self.input().image_format.clone()

    ##############################################

    def generate_data(self):

        """Method to update the output image content.

        Must be defined in subclass.

        """

        # self._logger.info(self.name)

        # Get the input and output
        # input_ = self.input()
        # output = self.output()

        # Get the corresponding image
        # input_.image
        # output.image

        raise NotImplementedError
