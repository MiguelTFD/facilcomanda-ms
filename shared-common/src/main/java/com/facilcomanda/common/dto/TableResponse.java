package com.facilcomanda.common.dto;
import com.facilcomanda.common.enums.TableState; public record TableResponse(Long id, String name, String description, TableState state, Integer chairs, Long organizationId, Long floorId, String floorName) {}
