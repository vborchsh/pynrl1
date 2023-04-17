
class nrPDSCH_config:
     def __init__(self):
          self._n_rb_size = 12
          self._n_size_bwp = 0
          self._n_start_bwp = 0
          self._mapping_type = "A"

          self._dmrs_typeA_pos = 2
          self._dmrs_len = 1
          self._dmrs_additional_pos = 1
          self._dmrs_conf_type = 2
          self._dmrs_port_set = 0
          self._num_CDM_groups_without_data = 1
          self._dmrs_NIDNSCID = 1
          self._dmrs_NSCID = 0
          self._PRB_set = list(range(0, self._n_size_bwp))
          self._symbol_allocation = [2, 12]

     @property
     def n_rb_size(self):
         return self._n_rb_size

     @property
     def n_size_bwp(self):
         return self._n_size_bwp

     @n_size_bwp.setter
     def n_size_bwp(self, size):
         assert size > 1 and size < 275, "The value must be in the range 1...275."
         self._n_size_bwp = size

     @property
     def n_start_bwp(self):
         return self._n_start_bwp

     @n_start_bwp.setter
     def n_start_bwp(self, start):
         assert start >= 0 and start < 2473, "The value must be in the range 0...2473."
         self._n_start_bwp = start

     @property
     def mapping_type(self):
         return self._mapping_type

     @mapping_type.setter
     def mapping_type(self, map_type):
         assert map_type in ["A", "B"], "The value must be in A or B"
         self._mapping_type = map_type

     @property
     def dmrs_typeA_pos(self):
         return self._dmrs_typeA_pos

     @dmrs_typeA_pos.setter
     def dmrs_typeA_pos(self, pos):
         assert pos in [2, 3], "The value must be 2 or 3"
         self._dmrs_typeA_pos = pos

     @property
     def dmrs_len(self):
         return self._dmrs_len

     @dmrs_len.setter
     def dmrs_len(self, length):
         assert length in [1, 2], "The value must be 1 or 2"
         self._dmrs_len = length

     @property
     def dmrs_additional_pos(self):
         return self._dmrs_additional_pos

     @dmrs_additional_pos.setter
     def dmrs_additional_pos(self, pos):
         assert pos in list(range(0,4)), "The value must be 0..3"
         self._dmrs_additional_pos = pos

     @property
     def dmrs_conf_type(self):
         return self._dmrs_conf_type

     @dmrs_conf_type.setter
     def dmrs_conf_type(self, conf_type):
         assert conf_type in [1, 2], "The value must be 1 or 2"
         self._dmrs_conf_type = conf_type

     @property
     def dmrs_port_set(self):
         assert False, "Not implemented!"
         return self._dmrs_port_set

     @dmrs_port_set.setter
     def dmrs_port_set(self, port_set):
         assert False, "Not implemented!"
         assert port_set in list(range(0, 11)), "The value must be 0..1"
         self._dmrs_port_set = port_set

     @property
     def num_CDM_groups_without_data(self):
         assert False, "Not implemented!"
         return self._num_CDM_groups_without_data

     @num_CDM_groups_without_data.setter
     def num_CDM_groups_without_data(self, num):
         assert False, "Not implemented!"
         assert num in list(range(0, 11)), "The value must be 0..1"
         self._num_CDM_groups_without_data = num

     @property
     def dmrs_NIDNSCID(self):
         return self._dmrs_NIDNSCID

     @dmrs_NIDNSCID.setter
     def dmrs_NIDNSCID(self, nid):
         assert nid > 0 and nid < 65535, "The value must be 0..65535"
         self._dmrs_NIDNSCID = nid

     @property
     def dmrs_NSCID(self):
         return self._dmrs_NIDNSCID

     @dmrs_NSCID.setter
     def dmrs_NSCID(self, nscid):
         assert nscid in [0, 1], "The value must be 0 or 1"
         self._dmrs_NSCID = nscid

     @property
     def PRB_set(self):
         return self._PRB_set

     @PRB_set.setter
     def PRB_set(self, prbset):
         assert min(prbset) >= 0 and max(prbset) < self._n_size_bwp, "The value must be 0..n_size_bwp"
         self._PRB_set = prbset

     @property
     def symbol_allocation(self):
         return self._symbol_allocation

     @symbol_allocation.setter
     def symbol_allocation(self, sym_list):
         # assert prbset > 0 and prbset < self._n_size_bwp, "The value must be 0..n_size_bwp"
         self._symbol_allocation = sym_list


class nrNumerology_config:
        def __init__(self):
            self._subcarrier_spacing = 15
            self._cyclic_prefix = "normal"

        @property
        def subcarrier_spacing(self):
            return self._subcarrier_spacing

        @subcarrier_spacing.setter
        def subcarrier_spacing(self, spacing):
            assert spacing in [15, 30, 60, 120, 240], "The value must be [15, 30, 60, 120, 240]"
            self._subcarrier_spacing = spacing

        @property
        def cyclic_prefix(self):
            return self._cyclic_prefix

        @cyclic_prefix.setter
        def cyclic_prefix(self, pref):
            assert pref in ["normal", "extended"], "The value must be [15, 30, 60, 120, 240]"
            self._cyclic_prefix = pref


class nrCarrier_config(nrNumerology_config):
        def __init__(self):
            self._n_cell_id = 1
            self._n_size_grid = 52
            self._n_start_grid = 0
            self._n_slot = 0
            self._n_frame = 0

            self.__symbols_per_slot = 0;
            self.__slots_per_subframe = 0;
            self.__slots_per_frame = 0;

        @property
        def symbols_per_slot(self):
            if self.cyclic_prefix == "normal":
                return 14
            else:
                return 12

        @property
        def slots_per_subframe(self):
            return self.subcarrier_spacing//15

        @property
        def slots_per_frame(self):
            return int(10*(self.subcarrier_spacing/15))

        @property
        def n_cell_id(self):
            return self._n_cell_id

        @n_cell_id.setter
        def n_cell_id(self, nid):
            assert nid >= 0 and nid <= 1007, "The value must be in the range 0...1007."
            self._n_cell_id = nid

        @property
        def n_size_grid(self):
            return self._n_size_grid

        @n_size_grid.setter
        def n_size_grid(self, size):
            assert size > 0 and size <= 275, "The value must be in the range 1...275."
            self._n_size_grid = size

        @property
        def n_start_grid(self):
            return self._n_start_grid

        @n_start_grid.setter
        def n_start_grid(self, start):
            assert start >= 0 and start <= 2199, "The value must be in the range 0...2999."
            self._n_start_grid = start

        @property
        def n_slot(self):
            return self._n_slot

        @n_slot.setter
        def n_slot(self, num):
            assert num >= 0, "The value must be scalar, nonnegative."
            self._n_slot = num

        @property
        def n_frame(self):
            return self._n_frame

        @n_frame.setter
        def n_frame(self, num):
            assert num >= 0, "The value must be scalar, nonnegative."
            self._n_frame = num