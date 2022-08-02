# Copyright 2013, Big Switch Networks, Inc.
#
# LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
# the following special exception:
#
# LOXI Exception
#
# As a special exception to the terms of the EPL, you may distribute libraries
# generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
# that copyright and licensing notices generated by LoxiGen are not altered or removed
# from the LoxiGen Libraries and the notice provided below is (i) included in
# the LoxiGen Libraries, if distributed in source code form and (ii) included in any
# documentation for the LoxiGen Libraries, if distributed in binary form.
#
# Notice: "Copyright 2013, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
#
# You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
# a copy of the EPL at:
#
# http://www.eclipse.org/legal/epl-v10.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# EPL for the specific language governing permissions and limitations
# under the EPL.

##
# @brief C code generation for LOXI type related maps
#

import c_gen.of_g_legacy as of_g
import sys
from generic_utils import *
import c_gen.type_maps as type_maps

def gen_type_data_header(out):
    out.write("""
/****************************************************************
 * Wire type/length functions.
 ****************************************************************/

extern void of_object_message_wire_length_get(of_object_t *obj, int *bytes);
extern void of_object_message_wire_length_set(of_object_t *obj, int bytes);

extern void of_oxm_wire_length_get(of_object_t *obj, int *bytes);

extern void of_tlv16_wire_length_get(of_object_t *obj, int *bytes);
extern void of_tlv16_wire_length_set(of_object_t *obj, int bytes);

/* Wire length is uint16 at front of structure */
extern void of_u16_len_wire_length_get(of_object_t *obj, int *bytes);
extern void of_u16_len_wire_length_set(of_object_t *obj, int bytes);

#define OF_OXM_LENGTH_GET(hdr) (((hdr) & 0xff) + 4)
#define OF_OXM_LENGTH_SET(hdr, val)                         \\
    (hdr) = ((hdr) & 0xffffff00) + (((val) - 4) & 0xff)

extern void of_packet_queue_wire_length_get(of_object_t *obj, int *bytes);
extern void of_packet_queue_wire_length_set(of_object_t *obj, int bytes);

extern void of_list_meter_band_stats_wire_length_get(of_object_t *obj,
                                                    int *bytes);
extern void of_meter_stats_wire_length_get(of_object_t *obj, int *bytes);
extern void of_meter_stats_wire_length_set(of_object_t *obj, int bytes);

extern void of_port_desc_wire_length_get(of_object_t *obj, int *bytes);
extern void of_port_desc_wire_length_set(of_object_t *obj, int bytes);

extern void of_port_stats_entry_wire_length_get(of_object_t *obj, int *bytes);
extern void of_port_stats_entry_wire_length_set(of_object_t *obj, int bytes);

extern void of_queue_stats_entry_wire_length_get(of_object_t *obj, int *bytes);
extern void of_queue_stats_entry_wire_length_set(of_object_t *obj, int bytes);

extern void of_queue_desc_wire_length_get(of_object_t *obj, int *bytes);
extern void of_queue_desc_wire_length_set(of_object_t *obj, int bytes);

""")


def gen_length_array(out):
    """
    Generate an array giving the lengths of all objects/versions
    @param out The file handle to which to write
    """
    out.write("""
/**
 * An array with the number of bytes in the fixed length part
 * of each OF object
 */
""")

    for version in of_g.of_version_range:
        out.write("""
static const int\nof_object_fixed_len_v%d[OF_OBJECT_COUNT] = {
    -1,   /* of_object is not instantiable */
""" % version)
        for i, cls in enumerate(of_g.all_class_order):
            comma = ","
            if i == len(of_g.all_class_order) - 1:
                comma = ""
            val = f"-1{comma}"
            if (cls, version) in of_g.base_length:
                val = str(of_g.base_length[(cls, version)]) + comma
            out.write("    %-5s /* %d: %s */\n" % (val, i + 1, cls))
        out.write("};\n")

    out.write("""
/**
 * Unified map of fixed length part of each object
 */
const int *const of_object_fixed_len[OF_VERSION_ARRAY_MAX] = {
    NULL,
""")
    for version in of_g.of_version_range:
        out.write("    of_object_fixed_len_v%d,\n" % version)
    out.write("""
};
""")
